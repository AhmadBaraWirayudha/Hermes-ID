"""Real-time signal engine for Hermes Analytics ID.

This module turns OSINT events, tension indicators, market observations, and watchlist
rules into scored real-time signals.
"""
from __future__ import annotations
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

from config import DB_PATH, ROOT, DATA_PROCESSED
from osint_monitor import init_osint_db, run_osint_cycle, monitor_pentagon_pizza_index, load_osint_events, load_tension_indicators, seed_default_osint_sources
from utils import now_stamp

REALTIME_SCHEMA = """
CREATE TABLE IF NOT EXISTS realtime_watchlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    pattern TEXT NOT NULL,
    category TEXT DEFAULT 'general',
    severity_weight REAL DEFAULT 1.0,
    active INTEGER NOT NULL DEFAULT 1,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS realtime_signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    observed_at TEXT NOT NULL,
    signal_type TEXT NOT NULL,
    source TEXT,
    category TEXT,
    title TEXT,
    url TEXT,
    score REAL DEFAULT 0,
    severity TEXT DEFAULT 'info',
    reason TEXT,
    payload TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(signal_type, source, url, title)
);

CREATE TABLE IF NOT EXISTS realtime_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    finished_at TEXT,
    status TEXT NOT NULL,
    osint_rows INTEGER DEFAULT 0,
    signal_rows INTEGER DEFAULT 0,
    message TEXT
);
"""

DEFAULT_WATCHLIST = [
    {"name": "IDX", "pattern": "idx|ihsg|bursa efek indonesia|stock exchange", "category": "capital_market", "severity_weight": 1.5, "active": True},
    {"name": "Bank Indonesia", "pattern": "bank indonesia|bi rate|interest rate|suku bunga|rupiah|idr", "category": "macro", "severity_weight": 1.7, "active": True},
    {"name": "Nickel", "pattern": "nickel|nikel|battery|ev supply chain", "category": "commodity", "severity_weight": 1.3, "active": True},
    {"name": "CPO", "pattern": "cpo|palm oil|minyak sawit|biodiesel", "category": "commodity", "severity_weight": 1.3, "active": True},
    {"name": "Coal", "pattern": "coal|batubara|energy security", "category": "commodity", "severity_weight": 1.2, "active": True},
    {"name": "Geopolitical tension", "pattern": "defcon|military|tension|war|conflict|sanction|geopolitik|militer", "category": "geopolitics", "severity_weight": 2.0, "active": True},
    {"name": "Regulatory", "pattern": "ojk|bappebti|kominfo|pdp|regulation|regulasi|aturan", "category": "regulatory", "severity_weight": 1.4, "active": True}
]


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def init_realtime_db():
    init_osint_db()
    with connect() as conn:
        conn.executescript(REALTIME_SCHEMA)


def seed_watchlist(path=None):
    init_realtime_db()
    path = Path(path) if path else ROOT / "config" / "realtime_watchlist.json"
    data = DEFAULT_WATCHLIST
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
    with connect() as conn:
        for row in data:
            conn.execute(
                """
                INSERT INTO realtime_watchlist(name, pattern, category, severity_weight, active, notes)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    pattern=excluded.pattern,
                    category=excluded.category,
                    severity_weight=excluded.severity_weight,
                    active=excluded.active,
                    notes=excluded.notes
                """,
                (row["name"], row["pattern"], row.get("category", "general"), float(row.get("severity_weight", 1.0)), 1 if row.get("active", True) else 0, row.get("notes", "")),
            )
    return len(data)


def load_watchlist(active_only=True):
    init_realtime_db()
    where = "WHERE active = 1" if active_only else ""
    with connect() as conn:
        return pd.read_sql_query(f"SELECT * FROM realtime_watchlist {where} ORDER BY category, name", conn)


def severity_from_score(score):
    if score >= 8:
        return "critical"
    if score >= 5:
        return "high"
    if score >= 3:
        return "medium"
    if score >= 1:
        return "low"
    return "info"


def score_event(text, watchlist):
    import re
    score = 0.0
    hits = []
    low = str(text or "").lower()
    for _, row in watchlist.iterrows():
        pattern = str(row["pattern"])
        try:
            matched = re.search(pattern, low, re.IGNORECASE) is not None
        except Exception:
            matched = pattern.lower() in low
        if matched:
            w = float(row.get("severity_weight", 1.0) or 1.0)
            score += w
            hits.append(row["name"])
    urgent_terms = ["breaking", "urgent", "darurat", "crisis", "krisis", "war", "conflict", "sanction", "rate hike", "kenaikan suku bunga"]
    for term in urgent_terms:
        if term in low:
            score += 1.5
            hits.append(term)
    return score, sorted(set(hits))


def compute_realtime_signals(limit=1000):
    init_realtime_db()
    watchlist = load_watchlist(active_only=True)
    if watchlist.empty:
        seed_watchlist()
        watchlist = load_watchlist(active_only=True)
    events = load_osint_events(limit=limit)
    signals = []
    for _, event in events.iterrows():
        text = " ".join([str(event.get("title") or ""), str(event.get("content") or ""), str(event.get("keywords") or "")])
        score, hits = score_event(text, watchlist)
        sentiment = event.get("sentiment_label")
        if sentiment == "negative":
            score += 1.0
        if hits or score >= 1:
            signals.append({
                "observed_at": event.get("observed_at") or utc_now(),
                "signal_type": "osint_event",
                "source": event.get("source"),
                "category": event.get("category"),
                "title": event.get("title"),
                "url": event.get("url"),
                "score": score,
                "severity": severity_from_score(score),
                "reason": ", ".join(hits) if hits else "sentiment or keyword signal",
                "payload": event.to_dict(),
            })
    tension = load_tension_indicators(limit=100)
    for _, row in tension.iterrows():
        text = " ".join([str(row.get("summary") or ""), str(row.get("level") or ""), str(row.get("score") or "")])
        score, hits = score_event(text, watchlist)
        if row.get("level"):
            try:
                level = float(row.get("level"))
                score += max(0, 6 - level)
            except Exception:
                score += 1
        if score > 0:
            signals.append({
                "observed_at": row.get("observed_at") or utc_now(),
                "signal_type": "tension_indicator",
                "source": row.get("source"),
                "category": "geopolitics",
                "title": row.get("indicator_name"),
                "url": row.get("url"),
                "score": score,
                "severity": severity_from_score(score),
                "reason": ", ".join(hits) if hits else "tension indicator",
                "payload": row.to_dict(),
            })
    return insert_signals(signals), pd.DataFrame(signals)


def insert_signals(signals):
    if not signals:
        return 0
    init_realtime_db()
    rows = []
    for s in signals:
        rows.append((
            s.get("observed_at") or utc_now(), s.get("signal_type"), s.get("source"), s.get("category"),
            s.get("title"), s.get("url"), float(s.get("score", 0) or 0), s.get("severity", "info"),
            s.get("reason"), json.dumps(s.get("payload", {}), ensure_ascii=False, default=str)
        ))
    with connect() as conn:
        conn.executemany(
            """
            INSERT INTO realtime_signals
            (observed_at, signal_type, source, category, title, url, score, severity, reason, payload)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(signal_type, source, url, title) DO UPDATE SET
                observed_at=excluded.observed_at,
                score=excluded.score,
                severity=excluded.severity,
                reason=excluded.reason,
                payload=excluded.payload
            """,
            rows,
        )
    return len(rows)


def run_realtime_cycle(include_pizza=True, source_limit=None):
    init_realtime_db()
    started = utc_now()
    osint_rows = 0
    signal_rows = 0
    messages = []
    status = "success"
    try:
        seed_default_osint_sources()
        seed_watchlist()
        osint_result = run_osint_cycle(limit=source_limit)
        if not osint_result.empty and "rows" in osint_result.columns:
            osint_rows = int(osint_result["rows"].sum())
        if include_pizza:
            try:
                monitor_pentagon_pizza_index()
            except Exception as e:
                messages.append(f"pizza monitor failed: {e}")
        signal_rows, signal_df = compute_realtime_signals()
    except Exception as e:
        status = "failed"
        messages.append(str(e))
    with connect() as conn:
        conn.execute(
            "INSERT INTO realtime_runs(started_at, finished_at, status, osint_rows, signal_rows, message) VALUES (?, ?, ?, ?, ?, ?)",
            (started, utc_now(), status, osint_rows, signal_rows, " | ".join(messages)),
        )
    return {"status": status, "osint_rows": osint_rows, "signal_rows": signal_rows, "message": " | ".join(messages)}


def load_realtime_signals(limit=500, severity=None):
    init_realtime_db()
    sql = "SELECT * FROM realtime_signals"
    params = []
    if severity:
        sql += " WHERE severity = ?"
        params.append(severity)
    sql += " ORDER BY score DESC, observed_at DESC LIMIT ?"
    params.append(int(limit))
    with connect() as conn:
        return pd.read_sql_query(sql, conn, params=params)


def load_realtime_runs(limit=100):
    init_realtime_db()
    with connect() as conn:
        return pd.read_sql_query("SELECT * FROM realtime_runs ORDER BY started_at DESC LIMIT ?", conn, params=(int(limit),))


def realtime_status():
    init_realtime_db()
    with connect() as conn:
        counts = {}
        for table in ["osint_events", "tension_indicators", "realtime_signals", "realtime_watchlist", "realtime_runs"]:
            try:
                counts[table] = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            except Exception:
                counts[table] = None
        latest = conn.execute("SELECT MAX(observed_at) FROM realtime_signals").fetchone()[0]
    return {"counts": counts, "latest_signal_at": latest}


def export_realtime_signals():
    df = load_realtime_signals(limit=10000)
    path = DATA_PROCESSED / f"{now_stamp()}_realtime_signals.csv"
    df.to_csv(path, index=False)
    return path
