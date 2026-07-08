"""Alerting and monitoring rules for market observations."""
import json
from pathlib import Path
import pandas as pd
from analytics import add_market_features
from quality import data_quality_report
from config import DATA_PROCESSED
from utils import now_stamp, format_idr

DEFAULT_RULES = {
    "stale_days_max": 14,
    "quality_score_min": 75,
    "zscore_abs_max": 2.5,
    "daily_pct_change_abs_max": 0.10,
    "price_min_by_item": {},
    "price_max_by_item": {},
}


def evaluate_alerts(df: pd.DataFrame, rules=None):
    rules = {**DEFAULT_RULES, **(rules or {})}
    alerts = []
    if df is None or df.empty:
        return pd.DataFrame([{"severity": "critical", "type": "no_data", "item": "ALL", "message": "No data available"}])
    q = data_quality_report(df)
    if q["score"] < rules["quality_score_min"]:
        alerts.append({"severity": "warning", "type": "quality_score", "item": "ALL", "message": f"Quality score {q['score']} below {rules['quality_score_min']}"})
    if q.get("stale_days") is not None and q["stale_days"] > rules["stale_days_max"]:
        alerts.append({"severity": "warning", "type": "stale_data", "item": "ALL", "message": f"Latest data is {q['stale_days']} days old"})

    featured = add_market_features(df)
    latest = featured.sort_values("date").groupby(["item", "region"], as_index=False).tail(1)
    for _, r in latest.iterrows():
        item = str(r.get("item"))
        region = str(r.get("region"))
        price = r.get("price")
        z = r.get("zscore_30d")
        pct = r.get("pct_change")
        if pd.notna(z) and abs(z) >= rules["zscore_abs_max"]:
            alerts.append({"severity": "warning", "type": "zscore_anomaly", "item": item, "region": region, "value": float(z), "message": f"{item} in {region} z-score {z:.2f}"})
        if pd.notna(pct) and abs(pct) >= rules["daily_pct_change_abs_max"]:
            alerts.append({"severity": "warning", "type": "pct_change", "item": item, "region": region, "value": float(pct), "message": f"{item} changed {pct:.1%}"})
        min_map = rules.get("price_min_by_item", {}) or {}
        max_map = rules.get("price_max_by_item", {}) or {}
        if item in min_map and pd.notna(price) and price < float(min_map[item]):
            alerts.append({"severity": "info", "type": "price_below_min", "item": item, "region": region, "value": float(price), "message": f"{item} below min: {format_idr(price)}"})
        if item in max_map and pd.notna(price) and price > float(max_map[item]):
            alerts.append({"severity": "critical", "type": "price_above_max", "item": item, "region": region, "value": float(price), "message": f"{item} above max: {format_idr(price)}"})
    if not alerts:
        alerts.append({"severity": "ok", "type": "healthy", "item": "ALL", "message": "No alert rules triggered"})
    return pd.DataFrame(alerts)


def save_alerts(alerts_df: pd.DataFrame, basename="alerts"):
    path = DATA_PROCESSED / f"{now_stamp()}_{basename}.csv"
    alerts_df.to_csv(path, index=False)
    return path


def load_rules_json(text):
    if not text or not str(text).strip():
        return DEFAULT_RULES.copy()
    return {**DEFAULT_RULES, **json.loads(text)}
