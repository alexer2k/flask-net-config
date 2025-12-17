@echo off
echo Installing Flask Network Configuration Service...

:: Check if Python is available
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

:: Install required packages
echo Installing required packages...
python -m pip install -r requirements.txt

:: Install the service
echo Installing Windows service...
python service_wrapper.py install

:: Start the service
echo Starting the service...
net start FlaskNetConfigService

echo Service installation complete!
echo You can access the application at http://localhost:5000
pause
