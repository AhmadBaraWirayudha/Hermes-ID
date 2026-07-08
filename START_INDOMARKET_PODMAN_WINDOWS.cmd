@echo off
setlocal
cd /d "%~dp0"
title IndoMarket Insight Podman Starter

echo ===================================================
echo IndoMarket Insight - Podman Start
echo ===================================================
echo.

where podman >nul 2>nul
if errorlevel 1 (
  echo Podman was not found.
  echo Install Podman Desktop first, then run this file again.
  echo https://podman-desktop.io/
  pause
  exit /b 1
)

where podman-compose >nul 2>nul
if errorlevel 1 (
  echo podman-compose was not found. Installing with Python pip...
  python -m pip install --user podman-compose
)

if not exist .env copy .env.example .env
podman-compose -f podman-compose.prod.yml up --build
pause
