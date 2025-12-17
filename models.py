from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import Permissions

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    # Bitwise permission mask
    role_mask = db.Column(db.Integer, default=Permissions.NONE)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, permission):
        """Bitwise check: if (UserMask & ReqMask) == ReqMask"""
        return (self.role_mask & permission) == permission

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    ip_address = db.Column(db.String(50))
    protocol = db.Column(db.String(10), default='telnet') # 'telnet' or 'http'
    port = db.Column(db.Integer, default=23)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    enable_password = db.Column(db.String(50))
    # Map this device to a Permission bit
    permission_bit = db.Column(db.Integer, default=0)

class Permission(db.Model):
    """Database model for managing permissions"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Integer, unique=True, nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Permission {self.name} ({self.value})>'

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    device_name = db.Column(db.String(50))
    action = db.Column(db.String(50))
    details = db.Column(db.Text)
