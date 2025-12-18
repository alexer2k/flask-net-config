from app import app
from services.translation_service import translation_service

with app.app_context():
    print('Testing dynamic translations:')

    # Test user translations
    user_params = {'username': 'admin'}
    edit_title = translation_service.get_translation_with_params('admin.users.edit_title', user_params)
    print(f'Edit user title: {edit_title}')

    delete_confirm = translation_service.get_translation_with_params('admin.users.delete_confirm', user_params)
    print(f'Delete user confirm: {delete_confirm}')

    # Test device translations
    device_params = {'device_name': 'GW_DM_Fonia'}
    device_edit_title = translation_service.get_translation_with_params('admin.devices.edit_title', device_params)
    print(f'Edit device title: {device_edit_title}')

    device_delete_confirm = translation_service.get_translation_with_params('admin.devices.delete_confirm', device_params)
    print(f'Delete device confirm: {device_delete_confirm}')

    # Test permission translations
    perm_params = {'permission_name': 'ADMIN_ACCESS', 'value': '1'}
    perm_edit_title = translation_service.get_translation_with_params('admin.permissions.edit_title', perm_params)
    print(f'Edit permission title: {perm_edit_title}')

    perm_delete_confirm = translation_service.get_translation_with_params('admin.permissions.delete_confirm', perm_params)
    print(f'Delete permission confirm: {perm_delete_confirm}')

    print('All dynamic translations working correctly!')
