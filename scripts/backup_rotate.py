"""Create backup and rotate old backups.
Usage: python scripts/backup_rotate.py --keep 20 --workspace
"""
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))
from backup import backup_sqlite, backup_workspace, BACKUP_DIR

parser = argparse.ArgumentParser()
parser.add_argument("--keep", type=int, default=20)
parser.add_argument("--workspace", action="store_true")
args = parser.parse_args()

created = backup_workspace(include_raw=False) if args.workspace else backup_sqlite()
print("created", created)
files = sorted([f for f in BACKUP_DIR.glob("*") if f.is_file()], key=lambda p: p.stat().st_mtime, reverse=True)
for f in files[args.keep:]:
    print("delete", f)
    f.unlink(missing_ok=True)
