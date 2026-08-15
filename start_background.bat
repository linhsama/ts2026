@echo off
title TS2026 Server - Background Launcher
cd /d "%~dp0"

set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "VBS_TARGET=%STARTUP_FOLDER%\ServerTS2026.vbs"

echo =================================================================
echo   STARTING TS2026 SERVER IN BACKGROUND (PORT 8080)
echo =================================================================
echo.

:: 1. Stop existing server if running on port 8080
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8080" ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
)

:: 2. Ensure run_background.vbs is up-to-date
> "%~dp0run_background.vbs" echo Set WshShell = CreateObject^("WScript.Shell"^)
>> "%~dp0run_background.vbs" echo WshShell.CurrentDirectory = "%~dp0"
>> "%~dp0run_background.vbs" echo WshShell.Run "pythonw " ^& Chr^(34^) ^& "%~dp0server.py" ^& Chr^(34^), 0, False

:: 3. Ensure Windows Startup script is present
> "%VBS_TARGET%" echo Set WshShell = CreateObject^("WScript.Shell"^)
>> "%VBS_TARGET%" echo WshShell.CurrentDirectory = "%~dp0"
>> "%VBS_TARGET%" echo WshShell.Run "pythonw " ^& Chr^(34^) ^& "%~dp0server.py" ^& Chr^(34^), 0, False

:: 4. Launch background process detached via WScript
start "" wscript.exe "%~dp0run_background.vbs"
timeout /t 2 >nul

:: 5. Verify server status
netstat -aon | findstr ":8080" | findstr "LISTENING" >nul
if %errorlevel% equ 0 (
    echo [OK] Server started successfully and is running in the background!
    echo.
    echo   * Local access address : http://127.0.0.1:8080/
    echo   * LAN client launcher   : ToolTS2026.html
    echo   * Server is detached   : You can safely close this window or Antigravity!
    echo   * Auto-Start is ready  : Server will auto-start with Windows.
) else (
    echo [!] Server is starting up. Please check http://127.0.0.1:8080/ in a moment.
)

echo.
echo To stop server: Run stop_server.bat
echo =================================================================
echo.
pause
