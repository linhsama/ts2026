@echo off
title Stop TS2026 Server
echo =================================================================
echo   STOPPING TS2026 SERVER (PORT 8080)
echo =================================================================
echo.

set "STOPPED=0"
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8080" ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
    set "STOPPED=1"
)

if "%STOPPED%"=="1" (
    echo [OK] Server process on port 8080 terminated successfully!
) else (
    echo [i] No active server process found on port 8080.
)

echo =================================================================
echo.
pause
