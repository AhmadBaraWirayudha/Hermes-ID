@echo off
setlocal
title IndoMarket Insight Stopper

echo Stopping Streamlit and Uvicorn processes for this user...
taskkill /IM streamlit.exe /F >nul 2>nul
taskkill /IM uvicorn.exe /F >nul 2>nul
wmic process where "commandline like '%%streamlit run app%%main.py%%'" call terminate >nul 2>nul
wmic process where "commandline like '%%uvicorn%%app.api:api%%'" call terminate >nul 2>nul

echo Done. If a terminal window remains open, you may close it manually.
pause
