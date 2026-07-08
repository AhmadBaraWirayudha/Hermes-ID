import pandas as pd

REQUIRED_COLUMNS = ["date", "source", "category", "item", "region", "price"]


def data_quality_report(df: pd.DataFrame) -> dict:
    if df is None or df.empty:
        return {
            "rows": 0,
            "missing_required_columns": REQUIRED_COLUMNS,
            "duplicate_keys": 0,
            "missing_price_pct": 0,
            "invalid_date_rows": 0,
            "negative_price_rows": 0,
            "stale_days": None,
            "score": 0,
            "issues": ["No data loaded"],
        }
    issues = []
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        issues.append(f"Missing required columns: {', '.join(missing_cols)}")
    work = df.copy()
    if "date" in work.columns:
        dates = pd.to_datetime(work["date"], errors="coerce")
        invalid_date_rows = int(dates.isna().sum())
        stale_days = None if dates.dropna().empty else int((pd.Timestamp.today().normalize() - dates.max().normalize()).days)
        if invalid_date_rows:
            issues.append(f"Invalid date rows: {invalid_date_rows}")
        if stale_days is not None and stale_days > 14:
            issues.append(f"Latest data is {stale_days} days old")
    else:
        invalid_date_rows, stale_days = 0, None
    key_cols = [c for c in ["date", "source", "category", "item", "region", "metric"] if c in work.columns]
    duplicate_keys = int(work.duplicated(key_cols).sum()) if key_cols else 0
    if duplicate_keys:
        issues.append(f"Duplicate logical keys: {duplicate_keys}")
    missing_price_pct = float(work["price"].isna().mean()) if "price" in work.columns else 1.0
    if missing_price_pct > 0.05:
        issues.append(f"Missing price ratio is high: {missing_price_pct:.1%}")
    negative_price_rows = int((pd.to_numeric(work.get("price", pd.Series(dtype=float)), errors="coerce") < 0).sum()) if "price" in work.columns else 0
    if negative_price_rows:
        issues.append(f"Negative price rows: {negative_price_rows}")
    score = 100
    score -= len(missing_cols) * 12
    score -= min(25, duplicate_keys)
    score -= min(30, int(missing_price_pct * 100))
    score -= min(20, invalid_date_rows)
    score -= min(20, negative_price_rows)
    if stale_days is not None and stale_days > 14:
        score -= min(20, stale_days // 7)
    return {
        "rows": len(work),
        "missing_required_columns": missing_cols,
        "duplicate_keys": duplicate_keys,
        "missing_price_pct": missing_price_pct,
        "invalid_date_rows": invalid_date_rows,
        "negative_price_rows": negative_price_rows,
        "stale_days": stale_days,
        "score": max(0, int(score)),
        "issues": issues or ["No major issues detected"],
    }


def column_profile(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame()
    rows = []
    for c in df.columns:
        s = df[c]
        rows.append({
            "column": c,
            "dtype": str(s.dtype),
            "missing": int(s.isna().sum()),
            "missing_pct": float(s.isna().mean()),
            "unique": int(s.nunique(dropna=True)),
            "sample": next((str(x) for x in s.dropna().head(1).tolist()), ""),
        })
    return pd.DataFrame(rows)
