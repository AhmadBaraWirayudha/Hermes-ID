import pandas as pd
import numpy as np


def add_market_features(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    out = df.copy()
    out["date"] = pd.to_datetime(out["date"], errors="coerce")
    out = out.sort_values(["item", "region", "date"])
    grp = out.groupby(["item", "region"], group_keys=False)
    out["price_change"] = grp["price"].diff()
    out["pct_change"] = grp["price"].pct_change()
    out["ma7"] = grp["price"].transform(lambda s: s.rolling(7, min_periods=1).mean())
    out["ma30"] = grp["price"].transform(lambda s: s.rolling(30, min_periods=1).mean())
    out["volatility_14d"] = grp["pct_change"].transform(lambda s: s.rolling(14, min_periods=3).std())
    out["zscore_30d"] = grp["price"].transform(lambda s: (s - s.rolling(30, min_periods=5).mean()) / s.rolling(30, min_periods=5).std())
    out["anomaly"] = out["zscore_30d"].abs() >= 2.5
    return out


def kpi_summary(df: pd.DataFrame) -> dict:
    if df.empty:
        return {"rows": 0, "items": 0, "regions": 0, "latest_date": "-", "avg_price": np.nan, "mom_7d": np.nan}
    featured = add_market_features(df)
    latest = featured.sort_values("date").groupby(["item", "region"], as_index=False).tail(1)
    return {
        "rows": len(df),
        "items": df["item"].nunique(),
        "regions": df["region"].nunique(),
        "latest_date": pd.to_datetime(df["date"]).max().date().isoformat(),
        "avg_price": latest["price"].mean(),
        "mom_7d": featured.groupby(["item", "region"])["pct_change"].tail(7).mean(),
        "anomalies": int(featured["anomaly"].sum()),
    }


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    tmp = df.copy()
    tmp["date"] = pd.to_datetime(tmp["date"])
    pivot = tmp.pivot_table(index="date", columns="item", values="price", aggfunc="mean")
    return pivot.pct_change().corr()
