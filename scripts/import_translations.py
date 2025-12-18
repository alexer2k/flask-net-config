"""
Script to import initial translations into the database
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Language, Translation

def import_translations():
    """Import initial translations into the database"""
    with app.app_context():
        # English (US) Translations
        en_us_translations = {
            # Login Page
            'login.title': 'Login',
            'login.username': 'Username',
            'login.password': 'Password',
            'login.button': 'Login',
            'login.invalid_credentials': 'Invalid Credentials',

            # Dashboard
            'dashboard.title': 'Select a Device',
            'dashboard.device_list': 'Device List',

            # Navigation
            'nav.brand': 'VG Manager',
            'nav.user': 'User: {username}',
            'nav.admin': 'Admin',
            'nav.logout': 'Logout',

            # Devices
            'devices.title': 'Manage Diversions',
            'devices.source': 'Incoming Number (Source)',
            'devices.current': 'Diverts To (Current)',
            'devices.new_destination': 'New Destination',
            'devices.action': 'Action',
            'devices.update_button': 'Update',
            'devices.no_rules': 'No diversion rules found for this device.',
            'devices.permission_error': 'You do not have permission for this task on this device.',
            'devices.success': 'Configuration updated successfully!',
            'devices.error': 'Error: {error}',

            # Admin - Users
            'admin.users.title': 'User Management',
            'admin.users.add_title': 'Add New User',
            'admin.users.username': 'Username',
            'admin.users.password': 'Password',
            'admin.users.permissions': 'Permissions',
            'admin.users.admin_access': 'Admin Access',
            'admin.users.task_divert': 'Task Divert',
            'admin.users.device_access': 'Device {device} Access',
            'admin.users.add_button': 'Add User',
            'admin.users.existing': 'Existing Users',
            'admin.users.edit_button': 'Edit',
            'admin.users.delete_button': 'Delete',
            'admin.users.edit_title': 'Edit User: {username}',
            'admin.users.new_password': 'New Password (leave blank to keep current)',
            'admin.users.save_changes': 'Save Changes',
            'admin.users.delete_confirm': 'Are you sure you want to delete user "{username}"?',
            'admin.users.cannot_delete_self': 'Cannot delete your own account',
            'admin.users.add_success': 'User added successfully',
            'admin.users.edit_success': 'User updated successfully',
            'admin.users.delete_success': 'User deleted successfully',
            'admin.users.username_exists': 'Username already exists',

            # Admin - Devices
            'admin.devices.title': 'Device Management',
            'admin.devices.add_title': 'Add New Device',
            'admin.devices.name': 'Device Name',
            'admin.devices.ip_address': 'IP Address',
            'admin.devices.protocol': 'Protocol',
            'admin.devices.port': 'Port',
            'admin.devices.username': 'Username',
            'admin.devices.password': 'Password',
            'admin.devices.enable_password': 'Enable Password',
            'admin.devices.permission_bit': 'Permission Bit',
            'admin.devices.add_button': 'Add Device',
            'admin.devices.existing': 'Existing Devices',
            'admin.devices.edit_button': 'Edit',
            'admin.devices.delete_button': 'Delete',
            'admin.devices.edit_title': 'Edit Device: {device_name}',
            'admin.devices.save_changes': 'Save Changes',
            'admin.devices.delete_confirm': 'Are you sure you want to delete device "{device_name}"?',
            'admin.devices.add_success': 'Device added successfully',
            'admin.devices.edit_success': 'Device updated successfully',
            'admin.devices.delete_success': 'Device deleted successfully',
            'admin.devices.name_exists': 'Device name already exists',

            # Admin - Permissions
            'admin.permissions.title': 'Permission Management',
            'admin.permissions.add_title': 'Add New Permission',
            'admin.permissions.name': 'Permission Name',
            'admin.permissions.value': 'Permission Value (bitwise)',
            'admin.permissions.description': 'Description',
            'admin.permissions.add_button': 'Add Permission',
            'admin.permissions.existing': 'Existing Permissions',
            'admin.permissions.edit_button': 'Edit',
            'admin.permissions.delete_button': 'Delete',
            'admin.permissions.edit_title': 'Edit Permission: {permission_name}',
            'admin.permissions.save_changes': 'Save Changes',
            'admin.permissions.delete_confirm': 'Are you sure you want to delete permission "{permission_name}" (value: {value})?',
            'admin.permissions.cannot_delete': 'Cannot delete permission: {users} users and {devices} devices are using it',
            'admin.permissions.add_success': 'Permission added successfully',
            'admin.permissions.edit_success': 'Permission updated successfully',
            'admin.permissions.delete_success': 'Permission deleted successfully',
            'admin.permissions.name_exists': 'Permission name already exists',
            'admin.permissions.value_exists': 'Permission value already exists',

            # Admin - Audit
            'admin.audit.title': 'Audit Log',
            'admin.audit.timestamp': 'Timestamp',
            'admin.audit.user': 'User',
            'admin.audit.device': 'Device',
            'admin.audit.action': 'Action',
            'admin.audit.details': 'Details',

            # Language Selector
            'language.selector': 'Select Language',
            'language.en_US': 'English',
            'language.it_IT': 'Italiano',
            'language.set_success': 'Language set to {language_code}',

            # General
            'general.loading': 'Loading...',
            'general.error': 'Error',
            'general.success': 'Success',
            'general.warning': 'Warning',
'general.info': 'Info',
'general.created': 'Created',
'general.action': 'Actions',
'general.no_results': 'No results found',
            'general.save': 'Save',
            'general.cancel': 'Cancel',
            'general.close': 'Close',
            'general.confirm': 'Confirm',
            'general.back': 'Back',
            'general.submit': 'Submit',
        }

        # Italian (IT) Translations
        it_it_translations = {
            # Login Page
            'login.title': 'Accesso',
            'login.username': 'Nome utente',
            'login.password': 'Password',
            'login.button': 'Accedi',
            'login.invalid_credentials': 'Credenziali non valide',

            # Dashboard
            'dashboard.title': 'Seleziona un Dispositivo',
            'dashboard.device_list': 'Lista Dispositivi',

            # Navigation
            'nav.brand': 'Gestione VG',
            'nav.user': 'Utente: {username}',
            'nav.admin': 'Amministrazione',
            'nav.logout': 'Esci',

            # Devices
            'devices.title': 'Gestisci Deviazioni',
            'devices.source': 'Numero Ingresso (Sorgente)',
            'devices.current': 'Deviazione Corrente (Corrente)',
            'devices.new_destination': 'Nuova Destinazione',
            'devices.action': 'Azione',
            'devices.update_button': 'Aggiorna',
            'devices.no_rules': 'Nessuna regola di deviazione trovata per questo dispositivo.',
            'devices.permission_error': 'Non hai il permesso per questo compito su questo dispositivo.',
            'devices.success': 'Configurazione aggiornata con successo!',
            'devices.error': 'Errore: {error}',

            # Admin - Users
            'admin.users.title': 'Gestione Utenti',
            'admin.users.add_title': 'Aggiungi Nuovo Utente',
            'admin.users.username': 'Nome utente',
            'admin.users.password': 'Password',
            'admin.users.permissions': 'Permessi',
            'admin.users.admin_access': 'Accesso Amministratore',
            'admin.users.task_divert': 'Deviazione Compiti',
            'admin.users.device_access': 'Accesso Dispositivo {device}',
            'admin.users.add_button': 'Aggiungi Utente',
            'admin.users.existing': 'Utenti Esistenti',
            'admin.users.edit_button': 'Modifica',
            'admin.users.delete_button': 'Elimina',
            'admin.users.edit_title': 'Modifica Utente: {username}',
            'admin.users.new_password': 'Nuova Password (lascia vuoto per mantenere corrente)',
            'admin.users.save_changes': 'Salva Modifiche',
            'admin.users.delete_confirm': 'Sei sicuro di voler eliminare l\'utente "{username}"?',
            'admin.users.cannot_delete_self': 'Non puoi eliminare il tuo account',
            'admin.users.add_success': 'Utente aggiunto con successo',
            'admin.users.edit_success': 'Utente aggiornato con successo',
            'admin.users.delete_success': 'Utente eliminato con successo',
            'admin.users.username_exists': 'Nome utente già esistente',

            # Admin - Devices
            'admin.devices.title': 'Gestione Dispositivi',
            'admin.devices.add_title': 'Aggiungi Nuovo Dispositivo',
            'admin.devices.name': 'Nome Dispositivo',
            'admin.devices.ip_address': 'Indirizzo IP',
            'admin.devices.protocol': 'Protocollo',
            'admin.devices.port': 'Porta',
            'admin.devices.username': 'Nome utente',
            'admin.devices.password': 'Password',
            'admin.devices.enable_password': 'Password Abilitazione',
            'admin.devices.permission_bit': 'Bit Permesso',
            'admin.devices.add_button': 'Aggiungi Dispositivo',
            'admin.devices.existing': 'Dispositivi Esistenti',
            'admin.devices.edit_button': 'Modifica',
            'admin.devices.delete_button': 'Elimina',
            'admin.devices.edit_title': 'Modifica Dispositivo: {device_name}',
            'admin.devices.save_changes': 'Salva Modifiche',
            'admin.devices.delete_confirm': 'Sei sicuro di voler eliminare il dispositivo "{device_name}"?',
            'admin.devices.add_success': 'Dispositivo aggiunto con successo',
            'admin.devices.edit_success': 'Dispositivo aggiornato con successo',
            'admin.devices.delete_success': 'Dispositivo eliminato con successo',
            'admin.devices.name_exists': 'Nome dispositivo già esistente',

            # Admin - Permissions
            'admin.permissions.title': 'Gestione Permessi',
            'admin.permissions.add_title': 'Aggiungi Nuovo Permesso',
            'admin.permissions.name': 'Nome Permesso',
            'admin.permissions.value': 'Valore Permesso (bitwise)',
            'admin.permissions.description': 'Descrizione',
            'admin.permissions.add_button': 'Aggiungi Permesso',
            'admin.permissions.existing': 'Permessi Esistenti',
            'admin.permissions.edit_button': 'Modifica',
            'admin.permissions.delete_button': 'Elimina',
            'admin.permissions.edit_title': 'Modifica Permesso: {permission_name}',
            'admin.permissions.save_changes': 'Salva Modifiche',
            'admin.permissions.delete_confirm': 'Sei sicuro di voler eliminare il permesso "{permission_name}" (valore: {value})?',
            'admin.permissions.cannot_delete': 'Impossibile eliminare il permesso: {users} utenti e {devices} dispositivi lo stanno utilizzando',
            'admin.permissions.add_success': 'Permesso aggiunto con successo',
            'admin.permissions.edit_success': 'Permesso aggiornato con successo',
            'admin.permissions.delete_success': 'Permesso eliminato con successo',
            'admin.permissions.name_exists': 'Nome permesso già esistente',
            'admin.permissions.value_exists': 'Valore permesso già esistente',

            # Admin - Audit
            'admin.audit.title': 'Registro Audit',
            'admin.audit.timestamp': 'Timestamp',
            'admin.audit.user': 'Utente',
            'admin.audit.device': 'Dispositivo',
            'admin.audit.action': 'Azione',
            'admin.audit.details': 'Dettagli',

            # Language Selector
            'language.selector': 'Seleziona Lingua',
            'language.en_US': 'Inglese',
            'language.it_IT': 'Italiano',
            'language.set_success': 'Lingua impostata su {language_code}',

            # General
            'general.loading': 'Caricamento...',
            'general.error': 'Errore',
            'general.success': 'Successo',
            'general.warning': 'Avviso',
            'general.info': 'Info',
            'general.save': 'Salva',
            'general.cancel': 'Annulla',
            'general.close': 'Chiudi',
            'general.confirm': 'Conferma',
            'general.back': 'Indietro',
            'general.submit': 'Invia',
        }

        # Get or create languages
        en_us_lang = Language.query.filter_by(code='en-US').first()
        it_it_lang = Language.query.filter_by(code='it-IT').first()

        if not en_us_lang or not it_it_lang:
            print("Error: Languages not found. Please run 'flask init-db' first.")
            return False

        # Import English translations
        print("Importing English (en-US) translations...")
        for key, value in en_us_translations.items():
            if not Translation.query.filter_by(key=key, language_code='en-US').first():
                translation = Translation(
                    key=key,
                    language_code='en-US',
                    value=value
                )
                db.session.add(translation)

        # Import Italian translations
        print("Importing Italian (it-IT) translations...")
        for key, value in it_it_translations.items():
            if not Translation.query.filter_by(key=key, language_code='it-IT').first():
                translation = Translation(
                    key=key,
                    language_code='it-IT',
                    value=value
                )
                db.session.add(translation)

        db.session.commit()
        print(f"Successfully imported {len(en_us_translations)} English and {len(it_it_translations)} Italian translations!")
        return True

if __name__ == '__main__':
    import_translations()
