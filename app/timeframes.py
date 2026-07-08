"""Time-window and resampling helpers."""
import pandas as pd

WINDOW_OPTIONS = {
    "All": None,
    "10 Year": pd.DateOffset(years=10),
    "5 Year": pd.DateOffset(years=5),
    "3 Year": pd.DateOffset(years=3),
    "2 Year": pd.DateOffset(years=2),
    "1 Year": pd.DateOffset(years=1),
    "YTD": "YTD",
}

FREQUENCY_OPTIONS = {
    "Daily": "D",
    "3 Day": "3D",
    "Weekly": "W",
    "Biweek": "2W",
    "Monthly": "MS",
    "Bimonthly": "2MS",
    "Quartal": "QS",
    "Quarterly": "QS",
    "Annual": "YS",
    "Biannual": "2QS",  # 6-month periods
}

REQUESTED_TIMEFRAMES = [
    "10 Year", "5 Year", "Biannual", "Annual", "Quartal", "Bimonthly",
    "Monthly", "Biweek", "Weekly", "3 Day", "Daily"
]


def apply_window(df, window_name="All", date_col="date"):
    if df.empty or window_name == "All" or window_name not in WINDOW_OPTIONS:
        return df
    out = df.copy()
    out[date_col] = pd.to_datetime(out[date_col], errors="coerce")
    max_date = out[date_col].max()
    if pd.isna(max_date):
        return out
    offset = WINDOW_OPTIONS[window_name]
    if offset == "YTD":
        start = pd.Timestamp(year=max_date.year, month=1, day=1)
    else:
        start = max_date - offset
    return out[out[date_col] >= start]


def resample_market(df, frequency_name="Daily", date_col="date"):
    if df.empty:
        return df
    freq = FREQUENCY_OPTIONS.get(frequency_name, "D")
    out = df.copy()
    out[date_col] = pd.to_datetime(out[date_col], errors="coerce")
    group_cols = [c for c in ["source", "category", "item", "region", "metric", "currency"] if c in out.columns]
    pieces = []
    for keys, g in out.dropna(subset=[date_col]).groupby(group_cols, dropna=False):
        rg = g.set_index(date_col).sort_index().resample(freq).agg({
            "price": "mean",
            "volume": "sum" if "volume" in g.columns else "size",
        }).reset_index()
        if not isinstance(keys, tuple):
            keys = (keys,)
        for col, val in zip(group_cols, keys):
            rg[col] = val
        pieces.append(rg)
    if not pieces:
        return out
    return pd.concat(pieces, ignore_index=True).sort_values(date_col)


def apply_timeframe(df, window_name="All", frequency_name="Daily", date_col="date"):
    return resample_market(apply_window(df, window_name, date_col), frequency_name, date_col)
