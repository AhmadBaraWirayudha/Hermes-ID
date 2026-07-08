"""Walk-forward forecast backtesting utilities."""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
from ml import prepare_series


def walk_forward_backtest(df, item, region=None, horizon=7, min_train=45, step=7):
    """Rolling-origin backtest for the RandomForest forecasting feature.

    Returns one row per predicted date with actual, prediction, error, and fold.
    """
    data = prepare_series(df, item, region)
    if len(data) < min_train + horizon:
        raise ValueError(f"Need at least {min_train + horizon} usable observations for backtest.")
    features = ["t", "dow", "month", "lag1", "lag7", "ma7"]
    rows = []
    fold = 0
    for train_end in range(min_train, len(data) - horizon + 1, step):
        fold += 1
        train = data.iloc[:train_end].copy()
        test = data.iloc[train_end:train_end + horizon].copy()
        model = RandomForestRegressor(n_estimators=250, random_state=42, min_samples_leaf=2)
        model.fit(train[features], train["price"])
        pred = model.predict(test[features])
        for i, (_, r) in enumerate(test.iterrows()):
            actual = float(r["price"])
            yhat = float(pred[i])
            rows.append({
                "fold": fold,
                "date": r["date"].date().isoformat() if hasattr(r["date"], "date") else str(r["date"]),
                "item": item,
                "region": region or "All",
                "actual": actual,
                "prediction": yhat,
                "error": yhat - actual,
                "abs_error": abs(yhat - actual),
                "ape": abs((yhat - actual) / actual) if actual else np.nan,
            })
    out = pd.DataFrame(rows)
    if out.empty:
        raise ValueError("Backtest produced no folds. Adjust horizon/min_train/step.")
    return out


def summarize_backtest(backtest_df):
    if backtest_df is None or backtest_df.empty:
        return {"folds": 0, "MAE": None, "MAPE": None, "Bias": None, "RMSE": None}
    return {
        "folds": int(backtest_df["fold"].nunique()),
        "rows": int(len(backtest_df)),
        "MAE": float(backtest_df["abs_error"].mean()),
        "MAPE": float(backtest_df["ape"].mean()),
        "Bias": float(backtest_df["error"].mean()),
        "RMSE": float(np.sqrt((backtest_df["error"] ** 2).mean())),
    }
