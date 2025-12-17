from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf.csrf import CSRFProtect
from config import Config, Permissions
from models import db, User, Device, AuditLog
from cisco_driver import CiscoVGDriver
from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)

# Initialize CSRF protection
csrf = CSRFProtect(app)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- CLI Command to init DB ---
@app.cli.command("init-db")
def init_db():
    db.create_all()
    # Create Admin
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', role_mask=Permissions.get_default_admin())
        admin.set_password('admin')
        db.session.add(admin)
    
    # Create the Voice Gateway from your text
    if not Device.query.filter_by(name='GW_DM_Fonia').first():
        vg = Device(
            name='GW_DM_Fonia',
            ip_address='10.255.1.2', # As per description
            username='cisco',
            password='insert_your_password',
            enable_password='insert_your_enable_password',
            permission_bit=Permissions.DEVICE_VG01
        )
        db.session.add(vg)
    
    db.session.commit()
    print("Database initialized.")

# --- Routes ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid Credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    # Show allowed devices
    devices = Device.query.all()
    allowed_devices = [d for d in devices if current_user.can(d.permission_bit)]
    return render_template('layout.html', content_type='dashboard', devices=allowed_devices)

@app.route('/diversion/<int:device_id>', methods=['GET', 'POST'])
@login_required
def diversion(device_id):
    # Permission Check
    device = Device.query.get_or_404(device_id)
    if not (current_user.can(Permissions.TASK_DIVERT) and current_user.can(device.permission_bit)):
        flash("You do not have permission for this task on this device.")
        return redirect(url_for('dashboard'))

    driver = CiscoVGDriver(device)
    
    # Handle Update
    if request.method == 'POST':
        rule_id = request.form['rule_id']
        raw_source = request.form['raw_source']
        new_dest = request.form['new_dest']
        
        try:
            # Execute on Cisco
            output = driver.update_diversion(rule_id, raw_source, new_dest)
            
            # Log to DB
            log = AuditLog(
                user_id=current_user.id,
                device_name=device.name,
                action="Change Diversion",
                details=f"Rule {rule_id}: {raw_source} -> {new_dest}"
            )
            db.session.add(log)
            db.session.commit()
            
            flash("Configuration updated successfully!")
        except Exception as e:
            flash(f"Error: {e}")

    # Load Current Config to display
    try:
        rules = driver.get_diversions()
    except Exception as e:
        flash(f"Could not connect to device: {e}")
        rules = []

    return render_template('diversion.html', device=device, rules=rules)

# Admin decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.can(Permissions.ADMIN_ACCESS):
            flash("Admin access required", "danger")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Admin Routes
@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    return redirect(url_for('admin_users'))

@app.route('/admin/users', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_users():
    if request.method == 'POST':
        # Add new user
        username = request.form['username']
        password = request.form['password']

        # Calculate permission mask
        permission_mask = 0
        permissions = request.form.getlist('permissions')
        for perm in permissions:
            permission_mask |= int(perm)

        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
        else:
            new_user = User(username=username, role_mask=permission_mask)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()

            # Log action
            log = AuditLog(
                user_id=current_user.id,
                device_name='SYSTEM',
                action="User Created",
                details=f"Created user {username} with permissions {permission_mask}"
            )
            db.session.add(log)
            db.session.commit()

            flash('User added successfully', 'success')

    users = User.query.all()
    return render_template('admin_users.html', users=users, active_page='users')

@app.route('/admin/users/<int:user_id>/edit', methods=['POST'])
@login_required
@admin_required
def admin_edit_user(user_id):
    user = User.query.get_or_404(user_id)

    username = request.form['username']
    password = request.form['password']

    # Update username if changed
    if user.username != username:
        if User.query.filter(User.username == username, User.id != user_id).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('admin_users'))
        user.username = username

    # Update password if provided
    if password:
        user.set_password(password)

    # Update permissions
    permission_mask = 0
    permissions = request.form.getlist('permissions')
    for perm in permissions:
        permission_mask |= int(perm)
    user.role_mask = permission_mask

    db.session.commit()

    # Log action
    log = AuditLog(
        user_id=current_user.id,
        device_name='SYSTEM',
        action="User Updated",
        details=f"Updated user {username} with permissions {permission_mask}"
    )
    db.session.add(log)
    db.session.commit()

    flash('User updated successfully', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)

    # Prevent deleting yourself
    if user_id == current_user.id:
        flash('Cannot delete your own account', 'danger')
        return redirect(url_for('admin_users'))

    username = user.username
    db.session.delete(user)
    db.session.commit()

    # Log action
    log = AuditLog(
        user_id=current_user.id,
        device_name='SYSTEM',
        action="User Deleted",
        details=f"Deleted user {username}"
    )
    db.session.add(log)
    db.session.commit()

    flash('User deleted successfully', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/devices', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_devices():
    if request.method == 'POST':
        # Add new device
        name = request.form['name']
        ip_address = request.form['ip_address']
        protocol = request.form['protocol']
        port = int(request.form['port'])
        username = request.form['username']
        password = request.form['password']
        enable_password = request.form['enable_password']
        permission_bit = int(request.form['permission_bit'])

        # Check if device exists
        if Device.query.filter_by(name=name).first():
            flash('Device name already exists', 'danger')
        else:
            new_device = Device(
                name=name,
                ip_address=ip_address,
                protocol=protocol,
                port=port,
                username=username,
                password=password,
                enable_password=enable_password,
                permission_bit=permission_bit
            )
            db.session.add(new_device)
            db.session.commit()

            # Log action
            log = AuditLog(
                user_id=current_user.id,
                device_name='SYSTEM',
                action="Device Created",
                details=f"Created device {name} with permission {permission_bit}"
            )
            db.session.add(log)
            db.session.commit()

            flash('Device added successfully', 'success')

    devices = Device.query.all()
    return render_template('admin_devices.html', devices=devices, active_page='devices')

@app.route('/admin/devices/<int:device_id>/edit', methods=['POST'])
@login_required
@admin_required
def admin_edit_device(device_id):
    device = Device.query.get_or_404(device_id)

    device.name = request.form['name']
    device.ip_address = request.form['ip_address']
    device.protocol = request.form['protocol']
    device.port = int(request.form['port'])
    device.username = request.form['username']
    device.password = request.form['password']
    device.enable_password = request.form['enable_password']
    device.permission_bit = int(request.form['permission_bit'])

    db.session.commit()

    # Log action
    log = AuditLog(
        user_id=current_user.id,
        device_name='SYSTEM',
        action="Device Updated",
        details=f"Updated device {device.name} with permission {device.permission_bit}"
    )
    db.session.add(log)
    db.session.commit()

    flash('Device updated successfully', 'success')
    return redirect(url_for('admin_devices'))

@app.route('/admin/devices/<int:device_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_device(device_id):
    device = Device.query.get_or_404(device_id)

    device_name = device.name
    db.session.delete(device)
    db.session.commit()

    # Log action
    log = AuditLog(
        user_id=current_user.id,
        device_name='SYSTEM',
        action="Device Deleted",
        details=f"Deleted device {device_name}"
    )
    db.session.add(log)
    db.session.commit()

    flash('Device deleted successfully', 'success')
    return redirect(url_for('admin_devices'))

@app.route('/admin/audit')
@login_required
@admin_required
def admin_audit():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return render_template('admin_audit.html', logs=logs, active_page='audit')

if __name__ == '__main__':
    # Threaded=True is useful for handling multiple slow telnet connections
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
