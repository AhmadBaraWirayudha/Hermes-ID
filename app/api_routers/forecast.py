from fastapi import APIRouter, Depends, HTTPException
from security import require_api_auth
from services.forecast_service import forecast_item, backtest_item
from schemas.forecast import ForecastResponse, BacktestResponse

router = APIRouter(prefix="/forecast", tags=["forecast"])

@router.get("/{item}", response_model=ForecastResponse)
def forecast(item: str, horizon: int = 14, region: str | None = None, _: dict = Depends(require_api_auth("forecast"))):
    try:
        result = forecast_item(item, horizon=horizon, region=region)
        return {"metrics": result["metrics"], "model_path": str(result["model_path"]), "forecast": result["forecast"].to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{item}/backtest", response_model=BacktestResponse)
def backtest(item: str, horizon: int = 7, min_train: int = 45, step: int = 7, region: str | None = None, _: dict = Depends(require_api_auth("forecast"))):
    try:
        result = backtest_item(item, horizon=horizon, min_train=min_train, step=step, region=region)
        return {"summary": result["summary"], "backtest": result["backtest"].to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
