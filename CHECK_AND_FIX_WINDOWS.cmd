@echo off
setlocal
cd /d "%~dp0"
title IndoMarket Insight Diagnostics

echo ===================================================
echo IndoMarket Insight - Check and Fix
echo ===================================================
echo.

call START_INDOMARKET_SETUP_WINDOWS.cmd
if errorlevel 1 (
  echo Setup failed before diagnostics could run.
  pause
  exit /b 1
)

echo Running doctor diagnostics...
".venv\Scripts\python.exe" scripts\doctor.py --fix

echo.
echo Running project validation...
".venv\Scripts\python.exe" scripts\validate_project.py

echo.
echo Diagnostics completed.
pause
