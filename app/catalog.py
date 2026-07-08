"""Data catalog and lineage summaries."""
from pathlib import Path
import pandas as pd
from config import DATA_RAW, DATA_PROCESSED, DB_PATH
from db import connect
from quality import column_profile


def file_catalog():
    rows = []
    for base, label in [(DATA_RAW, "raw"), (DATA_PROCESSED, "processed")]:
        if base.exists():
            for f in base.rglob("*"):
                if f.is_file():
                    rows.append({"zone": label, "file": str(f.relative_to(base.parent)), "suffix": f.suffix, "size_kb": round(f.stat().st_size/1024, 2), "modified": pd.to_datetime(f.stat().st_mtime, unit="s")})
    return pd.DataFrame(rows).sort_values("modified", ascending=False) if rows else pd.DataFrame()


def database_catalog():
    if not DB_PATH.exists():
        return pd.DataFrame()
    rows = []
    with connect() as conn:
        tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name", conn)
        for table in tables["name"]:
            try:
                count = pd.read_sql_query(f"SELECT COUNT(*) AS n FROM {table}", conn)["n"].iloc[0]
                rows.append({"table": table, "rows": int(count)})
            except Exception:
                rows.append({"table": table, "rows": None})
    return pd.DataFrame(rows)


def observation_profile(df):
    return column_profile(df)
