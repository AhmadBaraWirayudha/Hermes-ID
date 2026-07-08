import re
from datetime import datetime
import pytz
import pandas as pd
from config import TIMEZONE, DEFAULT_CURRENCY


def now_stamp():
    return datetime.now(pytz.timezone(TIMEZONE)).strftime("%Y%m%d_%H%M%S")


def clean_number(x):
    if pd.isna(x):
        return None
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x).strip()
    s = re.sub(r"[^0-9,.-]", "", s)
    # Indonesian numeric convention: 15.000,50 -> 15000.50
    if s.count(",") == 1 and (s.rfind(",") > s.rfind(".")):
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None


def format_idr(value):
    if pd.isna(value):
        return "-"
    return "Rp{:,.0f}".format(float(value)).replace(",", ".")


def normalize_market_df(df, source="manual", default_category="market", default_region="Indonesia"):
    df = df.copy()
    lower_map = {c: str(c).strip().lower() for c in df.columns}
    df.rename(columns=lower_map, inplace=True)

    synonyms = {
        "tanggal": "date", "time": "date", "periode": "date",
        "produk": "item", "komoditas": "item", "nama": "item", "ticker": "item",
        "harga": "price", "close": "price", "nilai": "price", "value": "price",
        "jumlah": "volume", "qty": "volume", "kuantitas": "volume",
        "wilayah": "region", "provinsi": "region", "kota": "region",
        "kategori": "category", "sektor": "category",
    }
    df.rename(columns={k: v for k, v in synonyms.items() if k in df.columns}, inplace=True)

    if "date" not in df.columns:
        df["date"] = pd.Timestamp.today().date().isoformat()
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date.astype(str)
    if "item" not in df.columns:
        df["item"] = "Unknown"
    if "price" not in df.columns:
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        df["price"] = df[numeric_cols[0]] if numeric_cols else None
    df["price"] = df["price"].apply(clean_number)
    if "volume" in df.columns:
        df["volume"] = df["volume"].apply(clean_number)
    else:
        df["volume"] = None
    if "category" not in df.columns:
        df["category"] = default_category
    if "region" not in df.columns:
        df["region"] = default_region
    df["source"] = source
    df["metric"] = df.get("metric", "price")
    df["currency"] = df.get("currency", DEFAULT_CURRENCY)
    df["raw_payload"] = None
    return df[["date", "source", "category", "item", "region", "price", "volume", "metric", "currency", "raw_payload"]]
