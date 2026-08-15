@echo off
title Install TS2026 Auto-Start & Run Background Server
cd /d "%~dp0"

set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "VBS_TARGET=%STARTUP_FOLDER%\ServerTS2026.vbs"

echo =================================================================
echo   TS2026 SERVER - 1-CLICK AUTO-START & BACKGROUND LAUNCHER
echo =================================================================
echo.

:: 1. Create startup script in Windows Startup folder (Auto-start on boot)
> "%VBS_TARGET%" echo Set WshShell = CreateObject^("WScript.Shell"^)
>> "%VBS_TARGET%" echo WshShell.CurrentDirectory = "%~dp0"
>> "%VBS_TARGET%" echo WshShell.Run "pythonw " ^& Chr^(34^) ^& "%~dp0server.py" ^& Chr^(34^), 0, False

echo [1/3] Created auto-start in Windows Startup folder:
echo       %VBS_TARGET%
echo.

:: 2. Synchronize run_background.vbs in project directory
> "%~dp0run_background.vbs" echo Set WshShell = CreateObject^("WScript.Shell"^)
>> "%~dp0run_background.vbs" echo WshShell.CurrentDirectory = "%~dp0"
>> "%~dp0run_background.vbs" echo WshShell.Run "pythonw " ^& Chr^(34^) ^& "%~dp0server.py" ^& Chr^(34^), 0, False

:: 3. Register with Windows Task Scheduler (as redundancy)
schtasks /create /tn "TS2026_Server_AutoStart" /tr "wscript.exe \"%~dp0run_background.vbs\"" /sc onlogon /f >nul 2>&1
if %errorlevel% equ 0 (
    echo [2/3] Registered task in Windows Task Scheduler successfully!
) else (
    echo [2/3] Configured via Windows Startup folder.
)
echo.

:: 4. Stop any existing server on port 8080
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8080" ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
)

:: 5. Start background server detached immediately
echo [3/3] Starting server in detached background mode...
start "" wscript.exe "%VBS_TARGET%"
timeout /t 2 >nul

:: 6. Verify server status
netstat -aon | findstr ":8080" | findstr "LISTENING" >nul
if %errorlevel% equ 0 (
    echo.
    echo =================================================================
    echo   [OK] SERVER IS ACTIVE AND RUNNING IN BACKGROUND (PORT 8080)!
    echo =================================================================
    echo.
    echo   * Local access address : http://127.0.0.1:8080/
    echo   * LAN client launcher   : ToolTS2026.html
    echo   * Server is detached   : You can safely close this window or Antigravity!
    echo   * Auto-Start is active : Server will auto-start every time PC turns on.
) else (
    echo [!] Server is starting up. Please access: http://127.0.0.1:8080/
)

echo.
echo To stop server: Run stop_server.bat
echo =================================================================
echo.
pause
