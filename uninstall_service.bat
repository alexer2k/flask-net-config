@echo off
echo Uninstalling Flask Network Configuration Service...

:: Stop the service if running
echo Stopping the service...
net stop FlaskNetConfigService >nul 2>nul

:: Uninstall the service
echo Uninstalling Windows service...
python service_wrapper.py uninstall

echo Service uninstallation complete!
pause
