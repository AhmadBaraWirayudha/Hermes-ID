"""Create a sanitized debug bundle for support and troubleshooting."""
from __future__ import annotations
import json
import platform
import sqlite3
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "processed"
SENSITIVE_NAMES = {".env", "users.json", "settings.json"}


def safe_read(path: Path, max_chars=200_000):
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:max_chars]
    except Exception as e:
        return f"Could not read {path}: {e}"


def sqlite_summary():
    db = ROOT / "data" / "indomarket.sqlite"
    if not db.exists():
        return {"exists": False}
    out = {"exists": True, "tables": {}}
    try:
        conn = sqlite3.connect(db)
        for name, in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall():
            try:
                n = conn.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
            except Exception:
                n = None
            out["tables"][name] = n
        conn.close()
    except Exception as e:
        out["error"] = str(e)
    return out


def build_bundle():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    bundle = OUT_DIR / f"debug_bundle_{stamp}.zip"
    manifest = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "python": sys.version,
        "sqlite": sqlite_summary(),
    }
    with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("manifest.json", json.dumps(manifest, indent=2, ensure_ascii=False))
        for rel in ["README.md", "CHANGELOG.md", "requirements.txt", "pyproject.toml", "START_HERE_ONE_CLICK.md"]:
            p = ROOT / rel
            if p.exists():
                z.writestr(rel, safe_read(p))
        for folder in ["logs", "docs/generated", "data/processed"]:
            base = ROOT / folder
            if not base.exists():
                continue
            for p in sorted(base.glob("*"))[-30:]:
                if p.is_file() and p.name not in SENSITIVE_NAMES and p.suffix.lower() in {".log", ".json", ".txt", ".md", ".csv"}:
                    z.write(p, p.relative_to(ROOT))
        for p in (ROOT / "config").glob("*.example.*"):
            z.write(p, p.relative_to(ROOT))
    return bundle


if __name__ == "__main__":
    print(build_bundle())
