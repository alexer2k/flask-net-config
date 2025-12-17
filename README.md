# Flask Network Configuration Service

This project provides a Flask application for managing network device configurations, packaged as a Windows service using Waitress for production deployment.

## Installation

### Prerequisites
- Windows 10/11 or Windows Server
- Python 3.7+
- Administrator privileges

### Installation Steps

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install the Windows service:**
   ```bash
   python service_wrapper.py install
   ```

   Or use the batch file:
   ```bash
   install_service.bat
   ```

3. **Start the service:**
   ```bash
   net start FlaskNetConfigService
   ```

## Usage

After installation, the service will run automatically on system startup. You can access the application at:

```
http://localhost:5000
```

### Service Management

- **Start service:** `net start FlaskNetConfigService`
- **Stop service:** `net stop FlaskNetConfigService`
- **Restart service:** `net stop FlaskNetConfigService && net start FlaskNetConfigService`
- **Uninstall service:** `python service_wrapper.py uninstall` or `uninstall_service.bat`

## Configuration

The service runs with the following configuration:
- **Host:** 0.0.0.0 (accessible from all network interfaces)
- **Port:** 5000
- **Threads:** 4 (for handling concurrent requests)
- **Production server:** Waitress (recommended for production)

## Development

For development purposes, you can still run the Flask app directly:
```bash
python app.py
```

## Troubleshooting

- **Service fails to start:** Check the Windows Event Log for detailed error messages
- **Port conflicts:** Ensure port 5000 is not being used by another application
- **Database issues:** The service automatically initializes the database on startup

## Building as Executable (Alternative)

If you prefer an executable file instead of a Windows service, you can use PyInstaller:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Create the executable:
   ```bash
   pyinstaller --onefile --windowed service_wrapper.py
   ```

3. The executable will be created in the `dist/` directory

## Notes

- The service runs with the same permissions as the user who installed it
- Database files are stored in the application directory
- Logs are written to the Windows Event Log
