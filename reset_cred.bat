@echo off
echo ================================================
echo   BASHIR AUTCONNECT!! YOUR HOSTEL NET MANAGER
echo ================================================
echo.
echo Stopping the background auto-login process...
taskkill /F /IM BashirSaab.exe /T >nul 2>&1

echo.
echo Deleting saved credentials...
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\wifi_creds.json" >nul 2>&1

echo.
echo Done! Your old password has been completely removed.
echo To enter your new password, just double-click your main Auto-Login app again.
echo.
pause