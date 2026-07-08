"""Copy core SQLite tables to PostgreSQL using DATABASE_URL.

Usage:
  export DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/indomarket
  python scripts/db/sqlite_to_postgres.py
"""
import os, sys, sqlite3
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "app"))
from storage_layer import get_sqlalchemy_engine
from config import DB_PATH

TABLES = ["sources", "market_observations", "scrape_runs"]

def main():
    if not os.getenv("DATABASE_URL", "").startswith("postgres"):
        raise SystemExit("Set DATABASE_URL to a PostgreSQL SQLAlchemy URL first.")
    engine = get_sqlalchemy_engine()
    src = sqlite3.connect(DB_PATH)
    for table in TABLES:
        df = pd.read_sql_query(f"SELECT * FROM {table}", src)
        print(f"copy {table}: {len(df)} rows")
        df.to_sql(table, engine, if_exists="append", index=False, method="multi", chunksize=1000)
    src.close()
    print("Migration copy complete. Verify counts before switching production traffic.")

if __name__ == "__main__":
    main()
