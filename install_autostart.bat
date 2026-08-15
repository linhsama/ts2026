@echo off
title Install TS2026 Server Windows Auto-Start
cd /d "%~dp0"

set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "VBS_TARGET=%STARTUP_FOLDER%\ServerTS2026.vbs"

echo =================================================================
echo   INSTALL AUTO-START TS2026 SERVER WITH WINDOWS
echo =================================================================
echo.

(
echo Set WshShell = CreateObject^("WScript.Shell"^)
echo WshShell.CurrentDirectory = "%~dp0"
echo WshShell.Run "python server.py", 0, False
) > "%VBS_TARGET%"

echo [OK] Auto-start successfully installed!
echo The TS2026 server will now start automatically in the background
echo whenever Windows boots up.
echo.
echo =================================================================
echo Starting Server now in background...
start "" "%VBS_TARGET%"
echo [OK] Server is running in the background on port 8080!
echo =================================================================
echo.
pause
