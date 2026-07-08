from pathlib import Path
import json
import pandas as pd
from config import DATA_PROCESSED
from utils import now_stamp, format_idr


def export_dataset(df: pd.DataFrame, basename="indomarket_export"):
    stamp = now_stamp()
    csv_path = DATA_PROCESSED / f"{stamp}_{basename}.csv"
    xlsx_path = DATA_PROCESSED / f"{stamp}_{basename}.xlsx"
    out = df.copy()
    if "price" in out.columns:
        out["price_idr"] = out["price"].apply(format_idr)
    out.to_csv(csv_path, index=False)
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        out.to_excel(writer, index=False, sheet_name="data")
        if "category" in out.columns and "price" in out.columns:
            summary = out.groupby("category", as_index=False).agg(rows=("price", "size"), avg_price=("price", "mean"), min_price=("price", "min"), max_price=("price", "max"))
            summary.to_excel(writer, index=False, sheet_name="summary")
    manifest_path = DATA_PROCESSED / f"{stamp}_{basename}_manifest.json"
    manifest = {
        "basename": basename,
        "created_at": stamp,
        "rows": int(len(out)),
        "columns": list(out.columns),
        "files": {"csv": str(csv_path), "xlsx": str(xlsx_path)},
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return csv_path, xlsx_path


def export_parquet(df: pd.DataFrame, basename="indomarket_export"):
    stamp = now_stamp()
    path = DATA_PROCESSED / f"{stamp}_{basename}.parquet"
    df.to_parquet(path, index=False)
    return path
