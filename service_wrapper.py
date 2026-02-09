import os
import sys
import time
import traceback

# Set up logging IMMEDIATELY to catch early crashes
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'service.log')

def log(msg):
    try:
        with open(log_file, 'a') as f:
            f.write(f"{time.ctime()}: {msg}\n")
    except:
        pass

log("-" * 50)
log(f"Script starting. Args: {sys.argv}")
log(f"Executable: {sys.executable}")
log(f"CWD: {os.getcwd()}")
log(f"sys.path: {sys.path}")

# Explicitly add venv site-packages if missing (fix for pythonservice.exe issue)
# Assuming standard venv structure: script in root, venv in .venv
base_dir = os.path.dirname(os.path.abspath(__file__))
venv_site = os.path.join(base_dir, '.venv', 'Lib', 'site-packages')
if os.path.exists(venv_site) and venv_site not in sys.path:
    log(f"Adding venv site-packages to path: {venv_site}")
    sys.path.insert(0, venv_site)

# Guard imports
try:
    log("Importing win32 modules...")
    import win32event
    import win32service
    import win32serviceutil
    log("Imported win32 modules.")
except ImportError as e:
    log(f"CRITICAL: Failed to import win32 modules: {e}")
    log(f"sys.path was: {sys.path}")
    # We can't proceed without win32serviceutil
    raise

# Guard servicemanager import (for debug mode safety)
try:
    import servicemanager
    _servicemanager_available = True
except ImportError:
    _servicemanager_available = False
    log("servicemanager module not found (normal for debug mode)")

try:
    log("Importing app and waitress...")
    from waitress import serve
    from app import app
    log("Imports successful.")
except Exception as e:
    log(f"Error importing app: {traceback.format_exc()}")
    app = None

class FlaskService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'FlaskNetConfigService'
    _svc_display_name_ = 'Flask Network Configuration Service'
    _svc_description_ = 'Flask application for network device configuration management'

    def __init__(self, args):
        log("Service initializing...")
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.server = None
        log("Service initialized.")

    def SvcStop(self):
        log("Service stopping...")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        log("Service stop signal sent.")

    def SvcDoRun(self):
        try:
            log("Service starting...")
            # Try to import servicemanager here
            try:
                import servicemanager
                if __name__ != '__main__':
                     # Only log to event viewer if running as service
                     servicemanager.LogMsg(
                        servicemanager.EVENTLOG_INFORMATION_TYPE,
                        servicemanager.PYS_SERVICE_STARTED,
                        (self._svc_name_, '')
                    )
            except ImportError:
                log("servicemanager module not found (normal for debug mode)")
            except Exception as ex:
                log(f"Failed to log to event viewer: {ex}")

            # Set current directory to the script directory
            script_dir = os.path.dirname(os.path.abspath(__file__))
            os.chdir(script_dir)
            log(f"Changed directory to {script_dir}")

            if app is None:
                log("App failed to import. Service cannot start.")
                return

            # Initialize database if needed
            log("Initializing database...")
            with app.app_context():
                from models import db
                db.create_all()
            log("Database initialized.")

            # Start Waitress server
            log("Starting Waitress server on port 5000...")
            serve(
                app,
                host='0.0.0.0',
                port=5000,
                threads=4,
                url_scheme='http'
            )
            log("Waitress server exited.")

        except Exception as e:
            log(f"Service crashed: {traceback.format_exc()}")
            try:
                import servicemanager
                if __name__ != '__main__':
                    servicemanager.LogErrorMsg(f"Service crashed: {e}")
            except:
                pass
            self.ReportServiceStatus(win32service.SERVICE_STOPPED)

if __name__ == '__main__':
    log(f"Running as script: {sys.argv}")
    
    if len(sys.argv) > 1 and sys.argv[1] == 'uninstall':
        sys.argv[1] = 'remove'

    if len(sys.argv) > 1 and (sys.argv[1] == 'debug' or sys.argv[1] == 'run'):
        log("Manual debug mode activated.")
        svc = FlaskService.__new__(FlaskService)
        svc.server = None
        svc.SvcDoRun()
    else:
        win32serviceutil.HandleCommandLine(FlaskService)
