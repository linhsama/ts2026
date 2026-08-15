@echo off
title Stop TS2026 Server
echo =================================================================
echo   STOPPING TS2026 SERVER (PORT 8080)
echo =================================================================
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8080"') do (
    taskkill /F /PID %%a >nul 2>&1
)
echo [OK] Server stopped successfully!
echo =================================================================
pause
