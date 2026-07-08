"""Compliance and geopolitical reference helpers."""
import json
from pathlib import Path
import pandas as pd
from config import ROOT


def load_standards_register():
    path = ROOT / "config" / "compliance" / "standards_register.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return pd.DataFrame(data.get("standards", []))


def load_indonesian_legal_domains():
    path = ROOT / "config" / "compliance" / "indonesian_legal_domains.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return pd.DataFrame({"domain": data.get("domains", [])})


def compliance_documents():
    docs = []
    for base in [ROOT / "docs" / "compliance", ROOT / "docs" / "policies", ROOT / "docs" / "geopolitics"]:
        if base.exists():
            for p in sorted(base.glob("*.md")):
                docs.append({"area": base.name, "document": p.name, "path": str(p.relative_to(ROOT))})
    return pd.DataFrame(docs)
