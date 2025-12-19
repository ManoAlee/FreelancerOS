@echo off
TITLE FreelancerOS - System Integrity Check
CLS
ECHO ========================================================
ECHO    FREELANCER OS - AUTOMATED VERIFICATION PROTOCOL
ECHO ========================================================
ECHO.

:: 1. Check Python
ECHO [1/4] Checking Python Environment...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO [ERROR] Python is not installed or not in PATH.
    ECHO Please install Python 3.x from python.org and check "Add to PATH".
    PAUSE
    EXIT /B
)
ECHO [OK] Python found.

:: 2. Check Dependencies
ECHO.
ECHO [2/4] Installing/Verifying Dependencies...
pip install -r projects/scraper_job/requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    ECHO [WARN] Some dependencies failed. Check internet connection.
) ELSE (
    ECHO [OK] Dependencies ready.
)

:: 3. Run Unit Tests
ECHO.
ECHO [3/4] Running Core Logic Tests...
python projects/FreelancerOS/tests.py
IF %ERRORLEVEL% NEQ 0 (
    ECHO [FAIL] Tests failed! Review errors above.
    PAUSE
    EXIT /B
)
ECHO [OK] All systems operational.

:: 4. Launch Dashboard
ECHO.
ECHO [4/4] Launching Mission Control...
ECHO Press any key to start the Dashboard...
PAUSE >nul
streamlit run projects/FreelancerOS/dashboard.py
