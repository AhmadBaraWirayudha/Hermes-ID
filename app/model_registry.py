"""Model registry based on saved joblib and metadata JSON files."""
import json
from pathlib import Path
import pandas as pd
from config import MODELS_DIR, DATA_PROCESSED
from utils import now_stamp

REGISTRY_PATH = MODELS_DIR / "model_registry.jsonl"


def register_model(name, model_path, item=None, metrics=None, params=None, notes=""):
    MODELS_DIR.mkdir(exist_ok=True)
    rec = {
        "created_at": now_stamp(),
        "name": name,
        "model_path": str(model_path),
        "item": item,
        "metrics": metrics or {},
        "params": params or {},
        "notes": notes,
    }
    with REGISTRY_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def list_models():
    rows = []
    if REGISTRY_PATH.exists():
        for line in REGISTRY_PATH.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try: rows.append(json.loads(line))
                except Exception: pass
    for f in MODELS_DIR.glob("*.joblib"):
        if not any(str(f) == r.get("model_path") for r in rows):
            rows.append({"created_at": None, "name": f.stem, "model_path": str(f), "item": None, "metrics": {}, "params": {}, "notes": "unregistered joblib"})
    flat = []
    for r in rows:
        rr = {k: v for k, v in r.items() if k not in ["metrics", "params"]}
        for k, v in (r.get("metrics") or {}).items(): rr[f"metric_{k}"] = v
        for k, v in (r.get("params") or {}).items(): rr[f"param_{k}"] = v
        flat.append(rr)
    return pd.DataFrame(flat)


def export_registry():
    df = list_models()
    path = DATA_PROCESSED / f"{now_stamp()}_model_registry.csv"
    df.to_csv(path, index=False)
    return path
