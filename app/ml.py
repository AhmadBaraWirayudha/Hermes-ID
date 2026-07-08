import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
from sklearn.model_selection import train_test_split
import joblib
from config import MODELS_DIR
try:
    from model_registry import register_model
except Exception:
    register_model = None


def prepare_series(df, item, region=None):
    data = df[df["item"] == item].copy()
    if region:
        data = data[data["region"] == region]
    data["date"] = pd.to_datetime(data["date"])
    data = data.sort_values("date")
    data = data.groupby("date", as_index=False)["price"].mean()
    data["t"] = np.arange(len(data))
    data["dow"] = data["date"].dt.dayofweek
    data["month"] = data["date"].dt.month
    data["lag1"] = data["price"].shift(1)
    data["lag7"] = data["price"].shift(7)
    data["ma7"] = data["price"].rolling(7).mean()
    return data.dropna()


def train_forecast_model(df, item, horizon=14, region=None):
    data = prepare_series(df, item, region)
    if len(data) < 20:
        raise ValueError("Need at least ~20 dated observations for ML forecast.")
    features = ["t", "dow", "month", "lag1", "lag7", "ma7"]
    X, y = data[features], data["price"]
    split = max(1, int(len(data) * 0.8))
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]
    model = RandomForestRegressor(n_estimators=300, random_state=42, min_samples_leaf=2)
    model.fit(X_train, y_train)
    pred = model.predict(X_test) if len(X_test) else model.predict(X_train)
    true = y_test if len(X_test) else y_train
    metrics = {
        "MAE": float(mean_absolute_error(true, pred)),
        "MAPE": float(mean_absolute_percentage_error(true, pred)),
    }

    history = data.copy()
    future_rows = []
    last_date = history["date"].max()
    for step in range(1, horizon + 1):
        next_date = last_date + pd.Timedelta(days=step)
        recent = history["price"].tail(7)
        row = {
            "t": len(history),
            "dow": next_date.dayofweek,
            "month": next_date.month,
            "lag1": history["price"].iloc[-1],
            "lag7": history["price"].iloc[-7] if len(history) >= 7 else history["price"].iloc[-1],
            "ma7": recent.mean(),
        }
        yhat = float(model.predict(pd.DataFrame([row]))[0])
        history = pd.concat([history, pd.DataFrame([{**row, "date": next_date, "price": yhat}])], ignore_index=True)
        future_rows.append({"date": next_date.date().isoformat(), "item": item, "forecast_price": yhat})

    model_path = MODELS_DIR / f"rf_forecast_{item.replace('/', '_').replace(' ', '_')}.joblib"
    joblib.dump(model, model_path)
    if register_model is not None:
        try:
            register_model("RandomForestForecaster", model_path, item=item, metrics=metrics, params={"horizon": horizon, "region": region}, notes="Auto-registered by train_forecast_model")
        except Exception:
            pass
    return pd.DataFrame(future_rows), metrics, model_path


def holt_linear_forecast(series, horizon=14, alpha=0.5, beta=0.2):
    values = pd.Series(series).dropna().astype(float).tolist()
    if len(values) < 2:
        return []
    level = values[0]
    trend = values[1] - values[0]
    for value in values[1:]:
        old_level = level
        level = alpha * value + (1 - alpha) * (level + trend)
        trend = beta * (level - old_level) + (1 - beta) * trend
    return [level + k * trend for k in range(1, horizon + 1)]
