@echo off
echo ========================================
echo DEPLOYING QUOTE INTELLIGENCE PLATFORM
echo ========================================

echo [1/4] Installing dependencies...
pip install -r requirements.txt

echo [2/4] Running ETL pipeline...
python pipeline/etl_pipeline.py

echo [3/4] Starting API server...
start "Quote API" cmd /k python api/main.py

timeout /t 3 /nobreak >nul

echo [4/4] Starting dashboard...
start "Quote Dashboard" cmd /k streamlit run dashboard/app.py

echo ========================================
echo DEPLOYMENT COMPLETE!
echo API: http://localhost:8000
echo Dashboard: http://localhost:8501
echo ========================================
echo.
echo Press any key to close this window...
pause >nul