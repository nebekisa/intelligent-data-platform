@echo off
echo ========================================
echo STARTING QUOTE INTELLIGENCE PLATFORM
echo ========================================

echo Starting API server...
start "Quote API" cmd /k python api/main.py

echo Waiting for API to be ready...
timeout /t 5 /nobreak >nul

echo Starting dashboard...
start "Quote Dashboard" cmd /k streamlit run dashboard/app.py

echo ========================================
echo SERVICES RUNNING:
echo API: http://localhost:8000
echo Dashboard: http://localhost:8501
echo ========================================
echo.
echo Close the terminal windows to stop services