@echo off
echo Fixing GitHub repository structure...
echo.

cd /d "c:\Users\LENOVO\OneDrive\Desktop\SEM 2 PROJECT MCA"

echo Creating new clean structure...
mkdir temp_project
cd temp_project

echo Copying files from fake_job_detector to root...
xcopy "..\fake_job_detector\*" "." /E /H /Y

echo.
echo Files copied successfully!
echo Now you need to:
echo 1. Delete your current GitHub repository
echo 2. Create a new one
echo 3. Push files from this temp_project folder
echo.
echo Location: c:\Users\LENOVO\OneDrive\Desktop\SEM 2 PROJECT MCA\temp_project
pause