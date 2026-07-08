"""Create a dependency availability report without installing anything."""
import importlib
import json
from datetime import datetime, timezone
from pathlib import Path
REQ = Path("requirements.txt")
mods = []
for line in REQ.read_text().splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    name = line.split("==")[0].split(">=")[0].split("~=")[0].split("[")[0].replace("-", "_")
    mods.append(name)
# common package-to-module corrections
aliases = {"beautifulsoup4": "bs4", "scikit_learn": "sklearn", "python_dateutil": "dateutil", "pillow": "PIL", "prometheus_client": "prometheus_client", "sentry_sdk": "sentry_sdk", "psycopg2_binary": "psycopg2"}
rows = []
for m in mods:
    module = aliases.get(m, m)
    try:
        mod = importlib.import_module(module)
        version = getattr(mod, "__version__", "unknown")
        ok = True
        detail = version
    except Exception as e:
        ok = False
        detail = str(e)
    rows.append({"package": m, "module": module, "installed": ok, "detail": detail})
out = {"created_at": datetime.now(timezone.utc).isoformat(), "dependencies": rows}
path = Path("data/processed/dependency_report.json")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(out, indent=2), encoding="utf-8")
print(path)
for r in rows:
    print(f"{'OK' if r['installed'] else 'MISS'} {r['package']} -> {r['module']} {r['detail']}")
