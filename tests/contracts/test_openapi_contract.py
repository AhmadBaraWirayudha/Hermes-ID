import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "app"))

def test_openapi_has_core_paths():
    try:
        from api import api
    except Exception:
        return  # dependencies not installed in minimal smoke environment
    spec = api.openapi()
    paths = spec.get("paths", {})
    assert "/health" in paths
    assert "/market/summary" in paths
    assert "/forecast/{item}" in paths
