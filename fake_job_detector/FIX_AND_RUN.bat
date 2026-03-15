@echo off
echo ========================================
echo   FIXING AND STARTING APP
echo ========================================
echo.

REM Stop any running Python processes
taskkill /F /IM python.exe 2>nul

REM Wait a moment
timeout /t 2 /nobreak >nul

echo Starting fresh...
python app.py

pause
