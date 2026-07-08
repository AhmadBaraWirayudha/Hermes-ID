"""Project diagnostics and light auto-fix tool."""
from __future__ import annotations
import argparse
import importlib
import json
import os
import platform
import re
import socket
import sqlite3
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app"
REPORT_DIR = ROOT / "data" / "processed"
REQUIRED_FILES = ["app/main.py", "app/api.py", "requirements.txt", "sql/schema.sql", "START_INDOMARKET_WINDOWS.cmd"]
REQUIRED_DIRS = ["data/raw", "data/processed", "models", "logs", "config", "backups"]
CORE_IMPORTS = ["pandas", "numpy", "streamlit", "plotly", "sklearn", "requests", "bs4"]
OPTIONAL_IMPORTS = ["fastapi", "uvicorn", "reportlab", "pytrends", "pyarrow", "sqlalchemy", "redis", "boto3", "prometheus_client"]
APP_IMPORTS = ["db", "scraper", "analytics", "quality", "alerts", "scenario", "data_studio", "sentiment", "security", "storage_layer"]
QUIET = False


def result(checks, name, ok, detail="", fix=""):
    checks.append({"name": name, "ok": bool(ok), "detail": str(detail), "fix": str(fix)})
    status = "OK" if ok else "FAIL"
    if not QUIET:
        print(f"[{status}] {name}: {detail}")


def port_open(port):
    s = socket.socket()
    s.settimeout(0.3)
    try:
        return s.connect_ex(("127.0.0.1", int(port))) == 0
    finally:
        s.close()


def main():
    parser = argparse.ArgumentParser(description="IndoMarket Insight diagnostics")
    parser.add_argument("--fix", action="store_true", help="Create missing folders and initialize DB when possible")
    parser.add_argument("--json", action="store_true", help="Print JSON only")
    args = parser.parse_args()
    global QUIET
    QUIET = bool(args.json)
    if not args.json:
        print("IndoMarket Insight Doctor")
        print("Root:", ROOT)
        print("Python:", sys.version.split()[0], platform.platform())
    checks = []

    for d in REQUIRED_DIRS:
        p = ROOT / d
        if args.fix:
            p.mkdir(parents=True, exist_ok=True)
        result(checks, f"directory {d}", p.exists(), p)

    for f in REQUIRED_FILES:
        p = ROOT / f
        result(checks, f"file {f}", p.exists(), p)

    for mod in CORE_IMPORTS:
        try:
            importlib.import_module(mod)
            result(checks, f"core dependency {mod}", True, "installed")
        except Exception as e:
            result(checks, f"core dependency {mod}", False, e, "Run pip install -r requirements.txt")

    for mod in OPTIONAL_IMPORTS:
        try:
            importlib.import_module(mod)
            result(checks, f"optional dependency {mod}", True, "installed")
        except Exception as e:
            result(checks, f"optional dependency {mod}", False, "not installed or unavailable", "Install requirements if feature is needed")

    sys.path.insert(0, str(APP))
    for mod in APP_IMPORTS:
        try:
            importlib.import_module(mod)
            result(checks, f"app import {mod}", True, "ok")
        except Exception as e:
            result(checks, f"app import {mod}", False, repr(e))

    if args.fix:
        try:
            sys.path.insert(0, str(APP))
            from db import init_db
            init_db()
            result(checks, "database init", True, "initialized")
        except Exception as e:
            result(checks, "database init", False, e)

    db_path = ROOT / "data" / "indomarket.sqlite"
    if db_path.exists():
        try:
            conn = sqlite3.connect(db_path)
            tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
            conn.close()
            required = {"market_observations", "sources", "scrape_runs"}
            result(checks, "sqlite schema", required.issubset(set(tables)), ",".join(tables))
        except Exception as e:
            result(checks, "sqlite schema", False, e)
    else:
        result(checks, "sqlite database", False, "missing", "Run python app/init_db.py")

    for port in [8501, 8000, 80, 9090, 3000]:
        result(checks, f"port {port}", True, "in use" if port_open(port) else "free")

    emoji_re = re.compile('[\U0001F300-\U0001FAFF\U00002700-\U000027BF\U00002600-\U000026FF]')
    em_dash = []
    emoji = []
    for p in ROOT.rglob("*"):
        if not p.is_file() or any(part in {".venv", "__pycache__", ".pytest_cache", ".git"} for part in p.parts):
            continue
        try:
            s = p.read_text(encoding="utf-8")
        except Exception:
            continue
        if "\u2014" in s:
            em_dash.append(str(p.relative_to(ROOT)))
        if emoji_re.search(s):
            emoji.append(str(p.relative_to(ROOT)))
    result(checks, "no em dash", not em_dash, em_dash[:10])
    result(checks, "no emoji", not emoji, emoji[:10])

    ok_count = sum(1 for c in checks if c["ok"])
    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "root": str(ROOT),
        "python": sys.version,
        "platform": platform.platform(),
        "ok": ok_count,
        "failed": len(checks) - ok_count,
        "checks": checks,
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    out = REPORT_DIR / f"doctor_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print("Summary:", ok_count, "ok,", len(checks) - ok_count, "failed")
        print("Report:", out)
    return 0 if report["failed"] == 0 else 2

if __name__ == "__main__":
    raise SystemExit(main())
