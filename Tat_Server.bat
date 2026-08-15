@echo off
title Dung Server TS2026 Dang Chay
echo =================================================================
echo   DUNG MAY CHU SERVER TS2026 DANG CHAY
echo =================================================================
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8080"') do (
    taskkill /F /PID %%a >nul 2>&1
)
echo [OK] Da dung Server thanh cong tren cong 8080!
echo =================================================================
pause
