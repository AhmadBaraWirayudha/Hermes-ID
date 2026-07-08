# Troubleshooting Matrix

| Symptom | Likely cause | Fix |
|---|---|---|
| Python not found | Python not installed or PATH missing | Install Python 3.10 or newer and enable Add Python to PATH |
| First run is slow | Dependencies are installing | Wait for installation to finish |
| Dashboard does not open | Streamlit not started or port blocked | Run `CHECK_AND_FIX_WINDOWS.cmd` or `python scripts/doctor.py --fix` |
| API health fails | API process not running | Use `START_INDOMARKET_WITH_API_WINDOWS.cmd` or `uvicorn app.api:api` |
| Port 8501 in use | Old dashboard still running | Run stop script, then start again |
| Report PDF fails | `reportlab` not installed | Run requirements install again |
| Google Trends fails | Rate limit or `pytrends` issue | Wait and retry with fewer keywords |
| Parquet export fails | `pyarrow` missing | Install requirements |
| Podman stack fails | Podman machine not running | Start Podman Desktop and retry |
| Data looks old | Sources not refreshed | Run active sources or import fresh CSV |
