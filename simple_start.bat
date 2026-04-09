@echo off
title Quote Intelligence Platform
color 0A

echo ========================================
echo    QUOTE INTELLIGENCE PLATFORM
echo ========================================
echo.

echo [1/2] Starting API server...
start "Quote API Server" cmd /k "python api/main.py"

echo Waiting for API to initialize...
timeout /t 3 /nobreak >nul

echo [2/2] Starting Dashboard...
start "Quote Dashboard" cmd /k "streamlit run dashboard/app.py"

echo Opening browser...
timeout /t 5 /nobreak >nul
start http://localhost:8501

echo.
echo ========================================
echo    SERVICES STARTED SUCCESSFULLY!
echo ========================================
echo.
echo API:        http://localhost:8000
echo Dashboard:  http://localhost:8501
echo Docs:       http://localhost:8000/docs
echo.
echo Close the terminal windows to stop services
echo ========================================
pause