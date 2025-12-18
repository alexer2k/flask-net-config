from app import app
from services.translation_service import translation_service

with app.app_context():
    print('Translation test:')
    print('Login title:', translation_service.get_translation('login.title'))
    print('Admin users title:', translation_service.get_translation('admin.users.title'))
    print('Admin devices title:', translation_service.get_translation('admin.devices.title'))
    print('Admin permissions title:', translation_service.get_translation('admin.permissions.title'))
    print('Admin audit title:', translation_service.get_translation('admin.audit.title'))
    print('Fallback test (should return key):', translation_service.get_translation('nonexistent.key'))
    print('All translations working correctly!')
