from fastapi import APIRouter, Depends, HTTPException
import pandas as pd
from security import require_api_auth
from osint_monitor import run_osint_cycle, load_osint_events, load_osint_runs, monitor_pentagon_pizza_index, load_tension_indicators, list_osint_sources, seed_default_osint_sources

router = APIRouter(prefix="/osint", tags=["osint"])

@router.get("/events")
def events(limit: int = 500, category: str | None = None, keyword: str | None = None, _: dict = Depends(require_api_auth("read"))):
    df = load_osint_events(limit=limit, category=category, keyword=keyword)
    return df.astype(object).where(pd.notnull(df), None).to_dict(orient="records")

@router.get("/runs")
def runs(limit: int = 200, _: dict = Depends(require_api_auth("read"))):
    df = load_osint_runs(limit=limit)
    return df.astype(object).where(pd.notnull(df), None).to_dict(orient="records")

@router.get("/sources")
def sources(active_only: bool = False, _: dict = Depends(require_api_auth("read"))):
    df = list_osint_sources(active_only=active_only)
    return df.astype(object).where(pd.notnull(df), None).to_dict(orient="records")

@router.post("/seed-sources")
def seed_sources(_: dict = Depends(require_api_auth("scrape"))):
    return {"imported": seed_default_osint_sources()}

@router.post("/run-cycle")
def run_cycle(_: dict = Depends(require_api_auth("scrape"))):
    df = run_osint_cycle()
    return df.to_dict(orient="records")

@router.post("/pentagon-pizza-index")
def pentagon_pizza(_: dict = Depends(require_api_auth("scrape"))):
    try:
        return monitor_pentagon_pizza_index()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tension-indicators")
def tension(limit: int = 100, _: dict = Depends(require_api_auth("read"))):
    df = load_tension_indicators(limit=limit)
    return df.astype(object).where(pd.notnull(df), None).to_dict(orient="records")
