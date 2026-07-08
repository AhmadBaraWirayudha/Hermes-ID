@echo off
setlocal
cd /d "%~dp0"
title IndoMarket Insight Frontend and API Starter

echo ===================================================
echo IndoMarket Insight - Frontend and API Start
echo ===================================================
echo.

call START_INDOMARKET_SETUP_WINDOWS.cmd
if errorlevel 1 goto fail

echo Starting dashboard...
start "IndoMarket Insight Dashboard" cmd /k "cd /d "%~dp0" && ".venv\Scripts\python.exe" -m streamlit run app\main.py --server.port 8501"

echo Starting API service...
start "IndoMarket Insight API" cmd /k "cd /d "%~dp0" && ".venv\Scripts\uvicorn.exe" app.api:api --host 0.0.0.0 --port 8000"

timeout /t 6 /nobreak >nul
start http://localhost:8501
start http://localhost:8000/health

echo.
echo Dashboard: http://localhost:8501
echo API:       http://localhost:8000/health
echo.
pause
exit /b 0

:fail
echo Setup failed. Try running CHECK_AND_FIX_WINDOWS.cmd for diagnostics.
pause
exit /b 1
