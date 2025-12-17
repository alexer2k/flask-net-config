import os

class Config:
    SECRET_KEY = 'super-secret-key-change-this'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Bitwise Permission Constants
class Permissions:
    NONE = 0
    ADMIN_ACCESS = 1         # 00000001
    TASK_DIVERT = 2          # 00000010
    DEVICE_VG01 = 4          # 00000100
    # Additional predefined permissions for extensibility
    DEVICE_VG02 = 8          # 00001000
    DEVICE_VG03 = 16         # 00010000
    DEVICE_VG04 = 32         # 00100000
    DEVICE_VG05 = 64         # 01000000
    DEVICE_VG06 = 128        # 10000000

    @staticmethod
    def get_default_admin():
        return Permissions.ADMIN_ACCESS | Permissions.TASK_DIVERT | Permissions.DEVICE_VG01

    @staticmethod
    def get_default_user():
        return Permissions.TASK_DIVERT | Permissions.DEVICE_VG01

    @staticmethod
    def get_all_device_permissions():
        """Return a list of all device permission tuples (value, name) from database"""
        from models import Permission
        try:
            permissions = Permission.query.filter(
                Permission.name.like('DEVICE_%')
            ).order_by(Permission.value).all()
            return [(p.value, p.name.replace('DEVICE_', '')) for p in permissions]
        except:
            # Fallback to hardcoded values if database is not available
            return [
                (Permissions.DEVICE_VG01, "VG01"),
                (Permissions.DEVICE_VG02, "VG02"),
                (Permissions.DEVICE_VG03, "VG03"),
                (Permissions.DEVICE_VG04, "VG04"),
                (Permissions.DEVICE_VG05, "VG05"),
                (Permissions.DEVICE_VG06, "VG06"),
            ]

    @staticmethod
    def get_permission_name(permission_value):
        """Get human-readable name for a permission value from database"""
        from models import Permission
        try:
            permission = Permission.query.filter_by(value=permission_value).first()
            if permission:
                return permission.description or permission.name.replace('_', ' ').title()
        except:
            pass

        # Fallback to hardcoded values if database is not available
        permission_map = {
            Permissions.ADMIN_ACCESS: "Admin Access",
            Permissions.TASK_DIVERT: "Task Divert",
            Permissions.DEVICE_VG01: "VG01 Access",
            Permissions.DEVICE_VG02: "VG02 Access",
            Permissions.DEVICE_VG03: "VG03 Access",
            Permissions.DEVICE_VG04: "VG04 Access",
            Permissions.DEVICE_VG05: "VG05 Access",
            Permissions.DEVICE_VG06: "VG06 Access",
        }
        return permission_map.get(permission_value, f"Permission {permission_value}")
