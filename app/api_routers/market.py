from fastapi import APIRouter, Depends
import pandas as pd
from security import require_api_auth
from repositories.observations_repo import list_observations
from services.market_service import get_market_summary, get_quality_report, get_alert_records, get_latest_records
from schemas.market import MarketSummaryOut, QualityReportOut, AlertOut

router = APIRouter(prefix="/market", tags=["market"])

@router.get("/summary", response_model=MarketSummaryOut)
def summary(_: dict = Depends(require_api_auth("read"))):
    return get_market_summary()

@router.get("/quality", response_model=QualityReportOut)
def quality(_: dict = Depends(require_api_auth("read"))):
    return get_quality_report()

@router.get("/latest")
def latest(_: dict = Depends(require_api_auth("read"))):
    df = get_latest_records()
    return df.astype(object).where(pd.notnull(df), None).to_dict(orient="records")

@router.get("/observations")
def observations(limit: int = 500, item: str | None = None, region: str | None = None, category: str | None = None, _: dict = Depends(require_api_auth("read"))):
    df = list_observations(limit=limit, item=item, region=region, category=category)
    return df.astype(object).where(pd.notnull(df), None).to_dict(orient="records")

@router.get("/alerts", response_model=list[AlertOut])
def alerts(_: dict = Depends(require_api_auth("read"))):
    return get_alert_records().to_dict(orient="records")
