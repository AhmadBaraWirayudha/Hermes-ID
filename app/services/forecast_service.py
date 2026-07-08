from db import load_observations
from ml import train_forecast_model
from backtesting import walk_forward_backtest, summarize_backtest


def forecast_item(item, horizon=14, region=None):
    forecast, metrics, model_path = train_forecast_model(load_observations(), item, horizon=horizon, region=region)
    return {"forecast": forecast, "metrics": metrics, "model_path": model_path}


def backtest_item(item, horizon=7, min_train=45, step=7, region=None):
    bt = walk_forward_backtest(load_observations(), item, region=region, horizon=horizon, min_train=min_train, step=step)
    return {"backtest": bt, "summary": summarize_backtest(bt)}
