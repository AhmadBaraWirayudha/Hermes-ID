# Start Here - One Click Use

## Windows 10 or Windows 11

Double-click this file:

```text
START_INDOMARKET_WINDOWS.cmd
```

It will:

1. create `.venv` if needed
2. install requirements
3. initialize the database
4. start the dashboard
5. open your browser at `http://localhost:8501`

## Windows with API service

Double-click:

```text
START_INDOMARKET_WITH_API_WINDOWS.cmd
```

This starts both:

```text
Dashboard: http://localhost:8501
API:       http://localhost:8000/health
```

## Stop on Windows

Double-click:

```text
STOP_INDOMARKET_WINDOWS.cmd
```

## Create desktop shortcut

Run PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\windows\create_desktop_shortcut.ps1
```

A shortcut named `IndoMarket Insight` will appear on your desktop.

## Windows with Podman

If you prefer the open-source Podman stack, install Podman Desktop and double-click:

```text
START_INDOMARKET_PODMAN_WINDOWS.cmd
```

## Linux

Run:

```bash
./START_INDOMARKET_LINUX.sh
```

Stop:

```bash
./STOP_INDOMARKET_LINUX.sh
```

## First run note

The first run can take several minutes because Python packages are installed. Later runs are faster.

## If something fails

Double-click:

```text
CHECK_AND_FIX_WINDOWS.cmd
```

Or run:

```bash
python scripts/doctor.py --fix
```

Then try starting again.

## Brand and developer

Brand: Hermes Analytics ID

Developed by: Ahmad Bara Wirayudha

GitHub: https://github.com/AhmadBaraWirayudha
