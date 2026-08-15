@echo off
title Cai Dat Tu Dong Khoi Dong Server TS2026 Cung Windows
cd /d "%~dp0"

set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "VBS_TARGET=%STARTUP_FOLDER%\ServerTS2026.vbs"

echo =================================================================
echo   CAI DAT TU DONG KHOI DONG SERVER TS2026 KHI BAT MAY TINH
echo =================================================================
echo.

(
echo Set WshShell = CreateObject^("WScript.Shell"^)
echo WshShell.CurrentDirectory = "%~dp0"
echo WshShell.Run "python server.py", 0, False
) > "%VBS_TARGET%"

echo [OK] Da cai dat thanh cong!
echo Tu gio tro di, moi khi ban bat may tinh, Server TS2026 se tu dong
echo khoi dong chay ngam trong he thong ma khong can phai mo cua so cmd.
echo.
echo =================================================================
echo Dang khoi dong Server ngay bay gio...
start "" "%VBS_TARGET%"
echo [OK] Server da duoc bat va dang chay ngam!
echo =================================================================
echo.
pause
