@echo off
title Open Windows Firewall for LAN Access - TS2026
cd /d "%~dp0"

echo =================================================================
echo   OPEN WINDOWS FIREWALL FOR PORT 8080 (LAN ACCESS) - TS2026
echo =================================================================
echo.

:: Check for administrative privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Requesting Administrator privileges to configure Windows Firewall...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo Adding Inbound Rule for TCP Port 8080...
netsh advfirewall firewall delete rule name="TS2026_Server_8080" >nul 2>&1
netsh advfirewall firewall add rule name="TS2026_Server_8080" dir=in action=allow protocol=TCP localport=8080 profile=any >nul 2>&1

echo.
echo =================================================================
echo  [SUCCESS] PORT 8080 HAS BEEN UNBLOCKED FOR ALL LAN / WI-FI NETWORKS!
echo =================================================================
echo.
echo Other computers and mobile devices on the same Wi-Fi / LAN can now:
echo   1. Open file: ToolTS2026.html
echo   2. Or enter the server IP in their browser: http://192.168.1.4:8080/
echo.
echo =================================================================
pause
