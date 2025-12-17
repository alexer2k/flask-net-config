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
    # Add more as needed:
    # DEVICE_VG02 = 8
    
    @staticmethod
    def get_default_admin():
        return Permissions.ADMIN_ACCESS | Permissions.TASK_DIVERT | Permissions.DEVICE_VG01

    @staticmethod
    def get_default_user():
        return Permissions.TASK_DIVERT | Permissions.DEVICE_VG01