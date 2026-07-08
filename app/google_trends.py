"""Google Trends extraction via optional pytrends dependency."""
import pandas as pd
from config import DATA_RAW, DATA_PROCESSED
from utils import now_stamp
from db import upsert_observations, log_scrape

PYTRENDS_TIMEFRAMES = {
    "10 Year": "today 10-y",
    "5 Year": "today 5-y",
    "Annual": "today 12-m",
    "Quartal": "today 3-m",
    "Quarterly": "today 3-m",
    "Monthly": "today 1-m",
    "Weekly": "now 7-d",
    "Daily": "now 7-d",
}


def _load_pytrends():
    try:
        from pytrends.request import TrendReq
        return TrendReq
    except Exception as exc:
        raise ImportError("Google Trends requires pytrends. Run: pip install pytrends") from exc


def fetch_google_trends(keywords, geo="ID", timeframe="today 5-y", category=0, gprop="", source_name="google_trends"):
    """Fetch Google Trends interest_over_time and store as market observations.

    keywords: list[str], max 5 per Google Trends request.
    price column stores Google Trends interest score 0-100.
    """
    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]
    if not keywords:
        raise ValueError("At least one keyword is required")
    if len(keywords) > 5:
        raise ValueError("Google Trends allows max 5 keywords per comparison request")
    TrendReq = _load_pytrends()
    pytrends = TrendReq(hl="id-ID", tz=420)
    pytrends.build_payload(keywords, cat=int(category or 0), timeframe=timeframe, geo=geo, gprop=gprop)
    raw = pytrends.interest_over_time().reset_index()
    if "isPartial" in raw.columns:
        raw = raw.drop(columns=["isPartial"])
    stamp = now_stamp()
    raw_path = DATA_RAW / f"{stamp}_{source_name}_google_trends_raw.csv"
    processed_path = DATA_PROCESSED / f"{stamp}_{source_name}_google_trends_processed.csv"
    raw.to_csv(raw_path, index=False)
    rows = []
    for kw in keywords:
        if kw not in raw.columns:
            continue
        for _, r in raw.iterrows():
            rows.append({
                "date": pd.to_datetime(r["date"]).date().isoformat(),
                "source": source_name,
                "category": "google_trends",
                "item": kw,
                "region": geo or "Global",
                "price": float(r[kw]) if pd.notna(r[kw]) else None,
                "volume": None,
                "metric": "search_interest",
                "currency": "INDEX_0_100",
                "raw_payload": None,
            })
    clean = pd.DataFrame(rows)
    clean.to_csv(processed_path, index=False)
    count = upsert_observations(clean)
    log_scrape(source_name, "success", count, raw_path, processed_path, f"google trends {keywords}")
    return clean, raw_path, processed_path
