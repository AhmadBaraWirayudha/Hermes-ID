@echo off
setlocal
cd /d "%~dp0"

echo Checking Python...
where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found.
  echo Install Python 3.10 or newer and enable Add Python to PATH.
  echo Download: https://www.python.org/downloads/
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo Creating virtual environment...
  python -m venv .venv
  if errorlevel 1 exit /b 1
)

echo Updating pip...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 exit /b 1

echo Installing requirements. This can take several minutes on first run...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 exit /b 1

echo Initializing database...
".venv\Scripts\python.exe" app\init_db.py
if errorlevel 1 exit /b 1

exit /b 0
