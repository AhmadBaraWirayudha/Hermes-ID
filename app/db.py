import sqlite3
from pathlib import Path
import pandas as pd
from config import DB_PATH, ROOT


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    schema = (ROOT / "sql" / "schema.sql").read_text(encoding="utf-8")
    with connect() as conn:
        conn.executescript(schema)


def upsert_observations(df: pd.DataFrame) -> int:
    if df.empty:
        return 0
    cols = ["date", "source", "category", "item", "region", "price", "volume", "metric", "currency", "raw_payload"]
    for col in cols:
        if col not in df.columns:
            df[col] = None
    rows = df[cols].where(pd.notnull(df[cols]), None).to_records(index=False).tolist()
    sql = """
    INSERT INTO market_observations
    (date, source, category, item, region, price, volume, metric, currency, raw_payload)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(date, source, category, item, region, metric)
    DO UPDATE SET price=excluded.price, volume=excluded.volume, currency=excluded.currency,
                  raw_payload=excluded.raw_payload, created_at=CURRENT_TIMESTAMP
    """
    with connect() as conn:
        conn.executemany(sql, rows)
    return len(rows)


def load_observations() -> pd.DataFrame:
    with connect() as conn:
        try:
            return pd.read_sql_query("SELECT * FROM market_observations ORDER BY date", conn, parse_dates=["date"])
        except Exception:
            return pd.DataFrame()


def log_scrape(source_name, status, rows_collected=0, raw_csv_path=None, processed_csv_path=None, message=""):
    with connect() as conn:
        conn.execute(
            """INSERT INTO scrape_runs(source_name, status, rows_collected, raw_csv_path, processed_csv_path, message, finished_at)
               VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)""",
            (source_name, status, rows_collected, str(raw_csv_path or ""), str(processed_csv_path or ""), message),
        )
