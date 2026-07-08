from typing import Optional
from pydantic import BaseModel

class ForecastPoint(BaseModel):
    date: str
    item: str
    forecast_price: float

class ForecastResponse(BaseModel):
    metrics: dict
    model_path: str
    forecast: list[ForecastPoint]

class BacktestPoint(BaseModel):
    fold: int
    date: str
    item: str
    region: str
    actual: float
    prediction: float
    error: float
    abs_error: float
    ape: Optional[float] = None

class BacktestResponse(BaseModel):
    summary: dict
    backtest: list[BacktestPoint]
