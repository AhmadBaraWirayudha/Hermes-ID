"""SQLite and project data backup/restore helpers."""
import shutil
import zipfile
from pathlib import Path
from config import DB_PATH, DATA_PROCESSED, DATA_RAW, ROOT
from utils import now_stamp

BACKUP_DIR = ROOT / "backups"
BACKUP_DIR.mkdir(exist_ok=True)


def backup_sqlite():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")
    out = BACKUP_DIR / f"{now_stamp()}_indomarket.sqlite.bak"
    shutil.copy2(DB_PATH, out)
    return out


def restore_sqlite(backup_file):
    if hasattr(backup_file, "read"):
        raw = backup_file.read()
        out_tmp = BACKUP_DIR / f"uploaded_{now_stamp()}_restore.sqlite"
        out_tmp.write_bytes(raw)
        src = out_tmp
    else:
        src = Path(backup_file)
    if not src.exists():
        raise FileNotFoundError(src)
    shutil.copy2(src, DB_PATH)
    return DB_PATH


def backup_workspace(include_raw=False):
    out = BACKUP_DIR / f"{now_stamp()}_indomarket_workspace.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for base in [DATA_PROCESSED] + ([DATA_RAW] if include_raw else []):
            if base.exists():
                for f in base.rglob("*"):
                    if f.is_file():
                        z.write(f, f.relative_to(ROOT))
        if DB_PATH.exists():
            z.write(DB_PATH, DB_PATH.relative_to(ROOT))
        for cfg in (ROOT / "config").glob("*.json"):
            z.write(cfg, cfg.relative_to(ROOT))
    return out
