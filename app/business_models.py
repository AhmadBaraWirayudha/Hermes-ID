"""Reusable business/finance model formulas for Indonesian market analysis."""
import math
import pandas as pd


def revenue_core(units, price):
    return float(units or 0) * float(price or 0)


def price_elasticity(pct_delta_quantity, pct_delta_price):
    pct_delta_price = float(pct_delta_price or 0)
    if pct_delta_price == 0:
        return None
    return float(pct_delta_quantity or 0) / pct_delta_price


def optimal_markup_price(marginal_cost, elasticity_demand):
    """P* = MC / (1 + 1/e). Demand elasticity should normally be negative."""
    e = float(elasticity_demand or 0)
    if e == 0 or (1 + 1 / e) == 0:
        return None
    return float(marginal_cost or 0) / (1 + 1 / e)


def roas(revenue_campaign, cost_campaign):
    cost_campaign = float(cost_campaign or 0)
    return None if cost_campaign == 0 else float(revenue_campaign or 0) / cost_campaign


def nrr(starting_mrr, expansion_mrr, contraction_mrr, churned_mrr):
    starting_mrr = float(starting_mrr or 0)
    if starting_mrr == 0:
        return None
    return (starting_mrr + float(expansion_mrr or 0) - float(contraction_mrr or 0) - float(churned_mrr or 0)) / starting_mrr * 100


def rule_of_40(yoy_growth_pct, ebitda_margin_pct):
    score = float(yoy_growth_pct or 0) + float(ebitda_margin_pct or 0)
    return score, score >= 40


def hhi(market_shares_pct):
    shares = [float(x) for x in market_shares_pct if str(x).strip() != ""]
    # Accept either percent numbers summing to 100 or decimals summing to 1.
    if sum(shares) <= 1.5:
        shares = [s * 100 for s in shares]
    return sum(s ** 2 for s in shares)


def single_exponential_smoothing(values, alpha=0.4):
    values = pd.Series(values).dropna().astype(float).tolist()
    if not values:
        return []
    out = [values[0]]
    for v in values[1:]:
        out.append(alpha * v + (1 - alpha) * out[-1])
    return out


def takt_time(available_production_time, customer_demand):
    demand = float(customer_demand or 0)
    return None if demand == 0 else float(available_production_time or 0) / demand


def capacity_utilization(total_output, max_capacity):
    max_capacity = float(max_capacity or 0)
    return None if max_capacity == 0 else float(total_output or 0) / max_capacity

# Extended holy-grail formula registry is available here for UI/CLI imports.
try:
    from holy_grail_formulas import FORMULA_REGISTRY as HOLY_GRAIL_FORMULAS
except Exception:
    HOLY_GRAIL_FORMULAS = {}
