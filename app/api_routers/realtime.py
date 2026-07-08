from fastapi import APIRouter, Depends
import pandas as pd
from security import require_api_auth
from realtime_engine import realtime_status, run_realtime_cycle, load_realtime_signals, load_realtime_runs, load_watchlist, seed_watchlist, export_realtime_signals

router = APIRouter(prefix="/realtime", tags=["realtime"])

@router.get("/status")
def status(_: dict = Depends(require_api_auth("read"))):
    return realtime_status()

@router.post("/run-cycle")
def run_cycle(include_pizza: bool = True, _: dict = Depends(require_api_auth("scrape"))):
    return run_realtime_cycle(include_pizza=include_pizza)

@router.get("/signals")
def signals(limit: int = 500, severity: str | None = None, _: dict = Depends(require_api_auth("read"))):
    df = load_realtime_signals(limit=limit, severity=severity)
    return df.astype(object).where(pd.notnull(df), None).to_dict(orient="records")

@router.get("/runs")
def runs(limit: int = 100, _: dict = Depends(require_api_auth("read"))):
    df = load_realtime_runs(limit=limit)
    return df.astype(object).where(pd.notnull(df), None).to_dict(orient="records")

@router.get("/watchlist")
def watchlist(active_only: bool = True, _: dict = Depends(require_api_auth("read"))):
    df = load_watchlist(active_only=active_only)
    return df.astype(object).where(pd.notnull(df), None).to_dict(orient="records")

@router.post("/seed-watchlist")
def seed(_: dict = Depends(require_api_auth("scrape"))):
    return {"seeded": seed_watchlist()}

@router.post("/export-signals")
def export(_: dict = Depends(require_api_auth("export"))):
    return {"path": str(export_realtime_signals())}
