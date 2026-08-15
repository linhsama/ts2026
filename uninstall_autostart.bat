@echo off
title Uninstall TS2026 Server Windows Auto-Start
set "VBS_TARGET=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\ServerTS2026.vbs"
if exist "%VBS_TARGET%" (
    del /f /q "%VBS_TARGET%"
    echo [OK] Auto-start removed successfully from Windows Startup!
) else (
    echo [!] Server is not currently installed in Windows Startup folder.
)
pause
