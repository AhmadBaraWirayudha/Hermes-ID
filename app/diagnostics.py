"""Diagnostics helpers used by Streamlit UI."""
import importlib
import socket
import sqlite3
from pathlib import Path
import pandas as pd
from config import ROOT, DB_PATH


def _port_status(port):
    s = socket.socket()
    s.settimeout(0.25)
    try:
        return "in use" if s.connect_ex(("127.0.0.1", int(port))) == 0 else "free"
    finally:
        s.close()


def diagnostic_table():
    rows = []
    for rel in ["app/main.py", "app/api.py", "requirements.txt", "sql/schema.sql", "START_INDOMARKET_WINDOWS.cmd"]:
        p = ROOT / rel
        rows.append({"area": "file", "name": rel, "status": "ok" if p.exists() else "missing", "detail": str(p)})
    for rel in ["data/raw", "data/processed", "models", "logs", "config", "backups"]:
        p = ROOT / rel
        rows.append({"area": "directory", "name": rel, "status": "ok" if p.exists() else "missing", "detail": str(p)})
    for mod in ["pandas", "streamlit", "plotly", "sklearn", "fastapi", "reportlab", "pytrends", "pyarrow"]:
        try:
            importlib.import_module(mod)
            status = "ok"
            detail = "installed"
        except Exception as e:
            status = "missing"
            detail = str(e)
        rows.append({"area": "dependency", "name": mod, "status": status, "detail": detail})
    if DB_PATH.exists():
        try:
            conn = sqlite3.connect(DB_PATH)
            tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
            conn.close()
            status = "ok" if {"market_observations", "sources", "scrape_runs"}.issubset(set(tables)) else "incomplete"
            detail = ", ".join(tables)
        except Exception as e:
            status = "error"
            detail = str(e)
    else:
        status = "missing"
        detail = str(DB_PATH)
    rows.append({"area": "database", "name": "sqlite", "status": status, "detail": detail})
    for port in [8501, 8000, 80, 9090, 3000]:
        rows.append({"area": "port", "name": str(port), "status": _port_status(port), "detail": "localhost"})
    return pd.DataFrame(rows)
