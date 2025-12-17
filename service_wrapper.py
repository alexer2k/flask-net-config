import os
import sys
import servicemanager
import win32event
import win32service
import win32serviceutil
import win32api
import win32con
import win32profile
from waitress import serve
from app import app

class FlaskService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'FlaskNetConfigService'
    _svc_display_name_ = 'Flask Network Configuration Service'
    _svc_description_ = 'Flask application for network device configuration management'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.server = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        if self.server:
            self.server.close()

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )

        # Set current directory to the script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)

        # Initialize database if needed
        with app.app_context():
            from models import db
            db.create_all()

        # Start Waitress server
        self.server = serve(
            app,
            host='0.0.0.0',
            port=5000,
            threads=4,
            url_scheme='http'
        )

        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

def install_service():
    # Get the path to the Python executable
    python_exe = sys.executable

    # Get the path to this script
    script_path = os.path.abspath(__file__)

    # Install the service
    win32serviceutil.InstallService(
        None,
        None,
        'FlaskNetConfigService',
        python_exe,
        ' '.join([script_path, 'run']),
        0,  # bRunInteractive
        None,
        None,
        None
    )

def uninstall_service():
    win32serviceutil.RemoveService('FlaskNetConfigService')

def run_service():
    win32serviceutil.HandleCommandLine(FlaskService)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'install':
            install_service()
        elif sys.argv[1] == 'uninstall':
            uninstall_service()
        elif sys.argv[1] == 'run':
            run_service()
        else:
            print("Usage: service_wrapper.py [install|uninstall|run]")
    else:
        print("Usage: service_wrapper.py [install|uninstall|run]")
