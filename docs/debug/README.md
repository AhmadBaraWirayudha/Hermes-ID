# Debugging and Diagnostics

Use these tools when the app does not start or a feature fails.

## Windows one-click diagnostics

Double-click:

```text
CHECK_AND_FIX_WINDOWS.cmd
```

## Command-line doctor

```bash
python scripts/doctor.py --fix
```

The doctor checks:

- required folders
- required files
- Python dependencies
- app imports
- SQLite schema
- common local ports
- no emoji and no em dash policy

A JSON report is written to `data/processed/`.

## Streamlit diagnostics page

Open the dashboard and go to:

```text
Diagnostics
```

## Common fixes

### Python not found on Windows

Install Python 3.10 or newer and enable Add Python to PATH.

### First run is slow

The first run installs dependencies. Later runs are faster.

### Port already in use

Stop old processes:

```text
STOP_INDOMARKET_WINDOWS.cmd
```

Linux:

```bash
./STOP_INDOMARKET_LINUX.sh
```

## New repair tools

```bash
python scripts/repair_project.py --demo
python scripts/create_debug_bundle.py
python scripts/port_report.py
python scripts/dependency_report.py
```

Windows one-click repair:

```text
REPAIR_INDOMARKET_WINDOWS.cmd
DEPENDENCY_REPORT_WINDOWS.cmd
```

See also:

```text
docs/debug/troubleshooting_matrix.md
```
