@echo off
setlocal
cd /d "%~dp0"
title Hermes Analytics ID Real-Time Monitor
call START_INDOMARKET_SETUP_WINDOWS.cmd
if errorlevel 1 goto fail
".venv\Scripts\python.exe" scripts\run_realtime_monitor.py --interval 300
exit /b 0
:fail
echo Setup failed.
pause
exit /b 1
