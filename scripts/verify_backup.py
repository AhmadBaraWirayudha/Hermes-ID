import argparse, sqlite3, sys
from pathlib import Path
parser = argparse.ArgumentParser()
parser.add_argument('backup')
args = parser.parse_args()
p = Path(args.backup)
if not p.exists():
    raise SystemExit(f'Missing backup: {p}')
try:
    conn = sqlite3.connect(p)
    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    conn.close()
except Exception as e:
    raise SystemExit(f'Invalid SQLite backup: {e}')
required = {'market_observations', 'sources', 'scrape_runs'}
missing = required - set(tables)
if missing:
    raise SystemExit(f'Backup missing tables: {missing}')
print('backup_ok', p, 'tables=', ','.join(tables))
