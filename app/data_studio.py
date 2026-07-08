"""Data transformation helpers for BI-style analysis."""
import pandas as pd


def growth_metrics(df, group_cols=("item", "region"), date_col="date", value_col="price"):
    if df is None or df.empty:
        return pd.DataFrame()
    out = df.copy()
    out[date_col] = pd.to_datetime(out[date_col], errors="coerce")
    out = out.sort_values(list(group_cols) + [date_col])
    grp = out.groupby(list(group_cols), group_keys=False)
    out["dod_change"] = grp[value_col].diff()
    out["dod_pct"] = grp[value_col].pct_change()
    out["wow_pct"] = grp[value_col].pct_change(7)
    out["mom_pct"] = grp[value_col].pct_change(30)
    out["qoq_pct"] = grp[value_col].pct_change(90)
    out["yoy_pct"] = grp[value_col].pct_change(365)
    out["rolling_7"] = grp[value_col].transform(lambda s: s.rolling(7, min_periods=1).mean())
    out["rolling_30"] = grp[value_col].transform(lambda s: s.rolling(30, min_periods=1).mean())
    return out


def rebase_index(df, base_date=None, group_cols=("item", "region"), date_col="date", value_col="price", base_value=100):
    if df is None or df.empty:
        return pd.DataFrame()
    out = df.copy()
    out[date_col] = pd.to_datetime(out[date_col], errors="coerce")
    out = out.sort_values(list(group_cols) + [date_col])
    pieces = []
    for _, g in out.groupby(list(group_cols), dropna=False):
        if base_date:
            bd = pd.to_datetime(base_date)
            candidates = g[g[date_col] >= bd]
            base = candidates[value_col].iloc[0] if not candidates.empty else g[value_col].iloc[0]
        else:
            base = g[value_col].iloc[0]
        g = g.copy()
        g["index_rebased"] = g[value_col] / base * base_value if base else None
        pieces.append(g)
    return pd.concat(pieces, ignore_index=True) if pieces else out


def pivot_market(df, index="date", columns="item", values="price", aggfunc="mean"):
    if df is None or df.empty:
        return pd.DataFrame()
    tmp = df.copy()
    if index == "date" and "date" in tmp.columns:
        tmp["date"] = pd.to_datetime(tmp["date"], errors="coerce")
    return tmp.pivot_table(index=index, columns=columns, values=values, aggfunc=aggfunc).reset_index()


def normalize_currency(df, fx_rate_to_idr=1.0, value_col="price", currency_col="currency", target="IDR"):
    out = df.copy()
    out[value_col] = pd.to_numeric(out[value_col], errors="coerce") * float(fx_rate_to_idr)
    out[currency_col] = target
    return out
