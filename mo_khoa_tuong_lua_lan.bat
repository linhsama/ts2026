@echo off
title Mo Khoa Tuong Lua Windows Cho Mang LAN - TS2026
cd /d "%~dp0"

echo =================================================================
echo   MO KHOA TUONG LUA WINDOWS (FIREWALL) CHO CONG 8080 - TS2026
echo =================================================================
echo.

:: Check for administrative privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Dang yeu cau quyen Administrator de mo Firewall...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo Dang them quyen truy cap Inbound tren cong 8080 TCP...
netsh advfirewall firewall delete rule name="TS2026_Server_8080" >nul 2>&1
netsh advfirewall firewall add rule name="TS2026_Server_8080" dir=in action=allow protocol=TCP localport=8080 profile=any >nul 2>&1

echo.
echo =================================================================
echo  [THANH CONG] DA MO KHOA CONG 8080 CHO TAT CA MANG LAN / WI-FI!
echo =================================================================
echo.
echo Cac may tinh / dien thoai khac trong mang LAN bay gio da co the:
echo   - Mo file: ToolTS2026.html
echo   - Hoac go tren trinh duyet: http://192.168.1.4:8080/
echo.
echo =================================================================
pause
