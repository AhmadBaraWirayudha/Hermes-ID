import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))
from api import api
out = Path("docs/architecture/openapi.json")
out.write_text(json.dumps(api.openapi(), indent=2), encoding="utf-8")
print(out)
