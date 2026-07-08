@echo off
setlocal
cd /d "%~dp0"
title IndoMarket Insight Starter

echo ===================================================
echo IndoMarket Insight - One Click Start
echo ===================================================
echo.
echo This will install or update dependencies, initialize the database,
echo start the dashboard, and open your browser.
echo.

call START_INDOMARKET_SETUP_WINDOWS.cmd
if errorlevel 1 goto fail

echo Starting dashboard...
start "IndoMarket Insight Dashboard" cmd /k "cd /d "%~dp0" && ".venv\Scripts\python.exe" -m streamlit run app\main.py --server.port 8501"

echo Waiting for dashboard to start...
timeout /t 6 /nobreak >nul
start http://localhost:8501

echo.
echo Dashboard started at http://localhost:8501
echo Keep the dashboard terminal open while using the app.
echo.
pause
exit /b 0

:fail
echo.
echo Setup failed. Check the messages above.
echo Try running CHECK_AND_FIX_WINDOWS.cmd for diagnostics.
pause
exit /b 1
