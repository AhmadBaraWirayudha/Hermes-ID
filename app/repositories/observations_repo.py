"""Repository layer for market observations.

Purpose: keep API/services independent from raw SQL/pandas storage details.
"""
import pandas as pd
from db import load_observations, upsert_observations, connect


def list_observations(limit=500, item=None, region=None, category=None):
    df = load_observations()
    if item:
        df = df[df["item"] == item]
    if region:
        df = df[df["region"] == region]
    if category:
        df = df[df["category"] == category]
    return df.tail(int(limit))


def latest_observations():
    df = load_observations()
    if df.empty:
        return df
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df.sort_values("date").groupby(["item", "region", "metric"], as_index=False).tail(1)


def save_observations(df):
    return upsert_observations(df)


def delete_observations_by_source(source):
    with connect() as conn:
        cur = conn.execute("DELETE FROM market_observations WHERE source = ?", (source,))
        return cur.rowcount
