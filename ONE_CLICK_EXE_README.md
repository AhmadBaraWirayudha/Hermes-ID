# One-click Windows `.exe` launcher

This project includes a Windows launcher that starts IndoMarket Insight with one double-click.

Because the app is a Python/Streamlit dashboard, the launcher does this automatically:

1. Finds the project folder.
2. Finds Python 3.10+ using `py`, `python`, or `python3`.
3. Creates `.venv` if it does not exist.
4. Installs `requirements.txt`.
5. Initializes the SQLite database.
6. Starts Streamlit on `http://localhost:8501`.
7. Opens your browser.

## Build the EXE on Windows

Open PowerShell in the `indomarket_insight` folder and run:

```powershell
powershell -ExecutionPolicy Bypass -File .\build_one_click_exe.ps1
```

Output:

```text
dist\IndoMarketInsight.exe
```

Then double-click:

```text
IndoMarketInsight.exe
```

## Create portable ZIP

After building the EXE:

```powershell
powershell -ExecutionPolicy Bypass -File .\package_windows_portable.ps1
```

Output:

```text
dist\IndoMarketInsight_Portable.zip
```

Send that ZIP to another Windows machine, extract it, and double-click:

```text
IndoMarketInsight.exe
```

## Requirements on the target Windows machine

- Windows 10/11 x64
- Python 3.10+ installed and added to PATH
- Internet connection on first run to install Python packages

The launcher itself is self-contained .NET, but the app still needs Python because it runs the Python dashboard.

## Troubleshooting

### Windows blocks the EXE

Right-click `IndoMarketInsight.exe` > Properties > Unblock.

### Python not found

Install Python from:

```text
https://www.python.org/downloads/
```

Enable:

```text
Add Python to PATH
```

### Dependencies fail to install

Run manually:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app\main.py
```
