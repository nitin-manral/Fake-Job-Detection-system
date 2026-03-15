@echo off
cd /d "%~dp0"
cls
echo ========================================
echo   AI Fake Job Detector - Starting...
echo ========================================
echo.

echo [1/4] Checking Python...
Improve the job analysis result section of the AI Fake Job Offer Detector.

After the analysis result, add the following sections below it:

1. **Verification Report**
   Show checks performed by the system such as:
   • Company website
   • Domain age
   • Email domain match
   • HTTPS security
   • Company presence

2. **Evidence Collected**
   Display the signals detected during analysis, for example:
   • Free email domain detected
   • Suspicious phrases in job description
   • Domain security information

3. **Color-Based Risk Indicator**
   Use clear colors for the result:
   • Red = High Risk / Likely Fake
   • Yellow = Suspicious / Medium Risk
   • Green = Safe / Likely Genuine

4. **Risk Score Bar**
   Show a visual risk meter or progress bar with the score percentage.

Keep all these sections **below the analysis result**, inside clean cards that match the dark dashboard UI.
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from python.org
    pause
    exit
)

echo.
echo [2/4] Cleaning old database...
if exist instance\job_detector.db (
    del /f /q instance\job_detector.db
    echo Database cleaned!
) else (
    echo No old database found.
)

echo.
echo [3/4] Installing dependencies...
pip install Flask Flask-SQLAlchemy scikit-learn python-whois reportlab --quiet

echo.
echo [4/4] Starting application...
echo.
echo ========================================
echo   Server starting at http://localhost:5000
echo   Press Ctrl+C to stop
echo ========================================
echo.

python app.py

pause
