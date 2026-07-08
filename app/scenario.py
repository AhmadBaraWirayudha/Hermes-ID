"""Scenario analysis and Monte Carlo simulation utilities."""
import numpy as np
import pandas as pd
from holy_grail_formulas import npv, terminal_value_gordon, value_at_risk, conditional_var


def monte_carlo_price_paths(start_price, days=252, simulations=1000, annual_drift=0.08, annual_volatility=0.25, seed=42):
    rng = np.random.default_rng(seed)
    dt = 1 / 252
    shocks = rng.normal((annual_drift - 0.5 * annual_volatility ** 2) * dt, annual_volatility * np.sqrt(dt), size=(days, simulations))
    paths = start_price * np.exp(np.cumsum(shocks, axis=0))
    return pd.DataFrame(paths, index=pd.RangeIndex(1, days + 1, name="day"))


def summarize_paths(paths: pd.DataFrame):
    final = paths.iloc[-1]
    returns = final / paths.iloc[0] - 1
    return {
        "simulations": int(paths.shape[1]),
        "days": int(paths.shape[0]),
        "final_mean": float(final.mean()),
        "final_median": float(final.median()),
        "final_p05": float(final.quantile(0.05)),
        "final_p95": float(final.quantile(0.95)),
        "return_mean": float(returns.mean()),
        "VaR_5pct_return": value_at_risk(returns, 0.05),
        "CVaR_5pct_return": conditional_var(returns, 0.05),
    }


def dcf_scenario(fcf0, growth_rates, discount_rate, terminal_growth, years=5):
    rows = []
    for g in growth_rates:
        fcfs = [fcf0 * ((1 + g) ** t) for t in range(1, years + 1)]
        tv = terminal_value_gordon(fcfs[-1] * (1 + terminal_growth), discount_rate, terminal_growth)
        enterprise = sum(cf / ((1 + discount_rate) ** i) for i, cf in enumerate(fcfs, start=1))
        if tv is not None:
            enterprise += tv / ((1 + discount_rate) ** years)
        rows.append({"growth_rate": g, "enterprise_value": enterprise, "terminal_value": tv})
    return pd.DataFrame(rows)
