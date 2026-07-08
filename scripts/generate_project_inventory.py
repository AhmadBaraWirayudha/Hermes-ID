from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "generated" / "project_inventory.md"
SKIP = {".venv", "__pycache__", ".pytest_cache", "node_modules", "dist", "build"}

rows = []
for p in sorted(ROOT.rglob("*")):
    rel = p.relative_to(ROOT)
    if any(part in SKIP for part in rel.parts):
        continue
    if p.is_file():
        rows.append((str(rel), p.suffix or "", round(p.stat().st_size/1024, 2)))
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", encoding="utf-8") as f:
    f.write("# Project Inventory\n\n")
    f.write(f"Generated: {datetime.now(timezone.utc).isoformat()}\n\n")
    f.write("| File | Type | Size KB |\n|---|---:|---:|\n")
    for rel, suffix, kb in rows:
        f.write(f"| `{rel}` | `{suffix}` | {kb} |\n")
print(OUT)
