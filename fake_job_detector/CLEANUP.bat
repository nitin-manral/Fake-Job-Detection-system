@echo off
echo Cleaning up old database...

taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

if exist instance rmdir /s /q instance
if exist job_detector.db del /f /q job_detector.db

echo Done! Now run START.bat
pause
