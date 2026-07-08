"""Import/export source registry JSON files."""
import json
from pathlib import Path
from source_registry import add_source, list_sources


def import_sources_json(path_or_file):
    if hasattr(path_or_file, "read"):
        raw = path_or_file.read()
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")
        data = json.loads(raw)
    else:
        data = json.loads(Path(path_or_file).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Source JSON must be a list of source objects")
    count = 0
    for src in data:
        add_source(
            src.get("name"),
            src.get("url"),
            src.get("source_type", "html_table"),
            src.get("table_index", 0),
            src.get("notes", ""),
            src.get("active", True),
        )
        count += 1
    return count


def export_sources_json(path):
    df = list_sources()
    records = df[["name", "url", "source_type", "table_index", "notes", "active"]].to_dict(orient="records") if not df.empty else []
    Path(path).write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
    return path
