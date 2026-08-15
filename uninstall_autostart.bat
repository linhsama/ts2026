@echo off
title Uninstall TS2026 Server Windows Auto-Start
set "VBS_TARGET=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\ServerTS2026.vbs"

echo =================================================================
echo   UNINSTALL TS2026 SERVER WINDOWS AUTO-START
echo =================================================================
echo.

if exist "%VBS_TARGET%" (
    del /f /q "%VBS_TARGET%"
    echo [OK] Removed startup script from Windows Startup folder!
) else (
    echo [!] No startup script found in Windows Startup folder.
)

schtasks /delete /tn "TS2026_Server_AutoStart" /f >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Removed task from Windows Task Scheduler!
)

echo.
echo =================================================================
echo   [DONE] AUTO-START HAS BEEN UNINSTALLED SUCCESSFULLY
echo =================================================================
echo.
pause
