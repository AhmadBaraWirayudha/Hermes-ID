@echo off
setlocal
cd /d "%~dp0"
title IndoMarket Insight Repair
call START_INDOMARKET_SETUP_WINDOWS.cmd
if errorlevel 1 goto fail
".venv\Scripts\python.exe" scripts\repair_project.py --demo
if errorlevel 1 goto fail
echo Repair completed.
pause
exit /b 0
:fail
echo Repair failed. Check messages above.
pause
exit /b 1
