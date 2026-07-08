@echo off
setlocal
cd /d "%~dp0"
call START_INDOMARKET_SETUP_WINDOWS.cmd
".venv\Scripts\python.exe" scripts\dependency_report.py
pause
