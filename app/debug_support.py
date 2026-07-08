"""Support helpers for diagnostics UI."""
from pathlib import Path
import pandas as pd
from config import ROOT, LOGS_DIR
from diagnostics import diagnostic_table


def recent_logs(max_lines=300):
    files = sorted(LOGS_DIR.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True) if LOGS_DIR.exists() else []
    if not files:
        return "No log files found."
    p = files[0]
    try:
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()[-max_lines:]
        return "\n".join(lines)
    except Exception as e:
        return f"Could not read log file {p}: {e}"


def diagnostic_summary():
    df = diagnostic_table()
    bad = df[~df["status"].isin(["ok", "free", "in use"])]
    return {"checks": len(df), "needs_attention": len(bad)}
