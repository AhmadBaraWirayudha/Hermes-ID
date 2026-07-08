"""Pydantic schemas for API contract stability."""
from typing import Optional, Any
from pydantic import BaseModel, Field

class MarketObservationOut(BaseModel):
    id: Optional[int] = None
    date: str
    source: str
    category: str
    item: str
    region: str = "Indonesia"
    price: Optional[float] = None
    volume: Optional[float] = None
    metric: str = "price"
    currency: str = "IDR"

class MarketSummaryOut(BaseModel):
    rows: int
    items: int
    regions: int
    latest_date: str | None = None
    avg_price: Optional[float] = None
    mom_7d: Optional[float] = None
    anomalies: Optional[int] = None

class AlertOut(BaseModel):
    severity: str
    type: str
    item: str
    message: str
    region: Optional[str] = None
    value: Optional[float] = None

class QualityReportOut(BaseModel):
    rows: int
    missing_required_columns: list[str]
    duplicate_keys: int
    missing_price_pct: float
    invalid_date_rows: int
    negative_price_rows: int
    stale_days: Optional[int] = None
    score: int
    issues: list[str]
