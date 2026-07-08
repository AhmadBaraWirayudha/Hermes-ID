"""Broad formula library inspired by holy-grail.pdf.

This module intentionally centralizes calculations across revenue, pricing, operations,
finance, risk, valuation, behavioral finance, and portfolio decisioning so the PDF concepts
are available as executable code. Functions are defensive: invalid divisions return None.
"""
import math
import statistics
import numpy as np
import pandas as pd


def _div(a, b):
    try:
        b = float(b)
        return None if b == 0 else float(a) / b
    except Exception:
        return None

def revenue_core(q, p): return float(q or 0) * float(p or 0)
def total_revenue(qs, ps): return sum(float(q)*float(p) for q,p in zip(qs, ps))
def price_elasticity(pct_delta_q, pct_delta_p): return _div(pct_delta_q, pct_delta_p)
def cross_price_elasticity(pct_delta_q_i, pct_delta_p_j): return _div(pct_delta_q_i, pct_delta_p_j)
def single_exponential_smoothing(values, alpha=0.4):
    vals=list(pd.Series(values).dropna().astype(float));
    if not vals: return []
    out=[vals[0]]
    for v in vals[1:]: out.append(alpha*v+(1-alpha)*out[-1])
    return out
def holt_linear(values, horizon=1, alpha=0.5, beta=0.2):
    vals=list(pd.Series(values).dropna().astype(float))
    if len(vals)<2: return []
    level, trend = vals[0], vals[1]-vals[0]
    for v in vals[1:]:
        old=level; level=alpha*v+(1-alpha)*(level+trend); trend=beta*(level-old)+(1-beta)*trend
    return [level+k*trend for k in range(1,horizon+1)]
def viral_coefficient(invites_per_user, conversion_rate): return float(invites_per_user or 0)*float(conversion_rate or 0)
def customer_base_next(n_prev, churn_rate, acquired, viral_k=0): return n_prev*(1-churn_rate)+acquired+n_prev*viral_k
def bass_adoption_rate(F_t, p, q): return (p+q*F_t)*(1-F_t)
def metcalfe_value(n, c=1): return c*n*(n-1)
def reed_value(n, c=1): return c*(2**n-n-1)
def mrr(subscription_rates): return sum(float(x or 0) for x in subscription_rates)
def nrr(starting_mrr, expansion_mrr, contraction_mrr, churned_mrr): return None if not starting_mrr else (starting_mrr+expansion_mrr-contraction_mrr-churned_mrr)/starting_mrr*100
def saas_magic_number(curr_arr, prev_arr, prev_sm_spend): return _div(curr_arr-prev_arr, prev_sm_spend)
def rule_of_40(growth_pct, ebitda_margin_pct):
    s=float(growth_pct or 0)+float(ebitda_margin_pct or 0); return s, s>=40
def roas(revenue_campaign, cost_campaign): return _div(revenue_campaign, cost_campaign)
def nps(promoters, detractors, total): return None if not total else (promoters-detractors)/total*100
def weibull_hazard(t, lam, p): return lam*p*((lam*t)**(p-1))
def revpac(arpu, occupancy_rate): return arpu*occupancy_rate
def occupancy(utilized, available): return _div(utilized, available)
def lerner_index(price, marginal_cost): return _div(price-marginal_cost, price)
def optimal_markup_price(mc, elasticity_demand):
    e=float(elasticity_demand or 0); den=1+1/e if e else 0; return None if den==0 else mc/den
def marginal_revenue(price, elasticity): return price*(1+1/elasticity) if elasticity else None
def cobb_douglas(A, L, K, alpha, beta): return A*(L**alpha)*(K**beta)
def returns_to_scale(alpha,beta):
    s=alpha+beta; return "increasing" if s>1 else "decreasing" if s<1 else "constant"
def hhi(shares):
    vals=[float(x) for x in shares];
    if sum(vals)<=1.5: vals=[100*x for x in vals]
    return sum(x*x for x in vals)
def taylor_rule(r_star, pi_t, pi_star, output_gap): return r_star+pi_t+0.5*(pi_t-pi_star)+0.5*output_gap
def gini(x):
    vals=np.array(list(x), dtype=float); n=len(vals)
    return None if n==0 or vals.mean()==0 else np.abs(vals[:,None]-vals[None,:]).sum()/(2*n*n*vals.mean())
def phillips_curve(pi_expected, unemployment, natural_unemployment, beta, shock=0): return pi_expected-beta*(unemployment-natural_unemployment)+shock
def uip_fx_expected(spot, domestic_rate, foreign_rate): return spot*(1+domestic_rate)/(1+foreign_rate)
def ppp_fx_change(pi_domestic, pi_foreign): return pi_domestic-pi_foreign

def fixed_cost(*costs): return sum(float(x or 0) for x in costs)
def variable_cost(qs, variable_costs): return sum(float(q)*float(v) for q,v in zip(qs, variable_costs))
def activity_rate(pool_cost, driver_capacity): return _div(pool_cost, driver_capacity)
def allocated_overhead(activity_rates, consumptions): return sum(r*c for r,c in zip(activity_rates, consumptions))
def capacity_utilization(output, max_capacity): return _div(output, max_capacity)
def learning_curve_cost(c1, n, b): return c1*(n**(math.log(b)/math.log(2)))
def littles_law(arrival_rate, wait_time): return arrival_rate*wait_time
def mm1_wait_time(lam, mu): return _div(1, mu-lam) if mu>lam else None
def mm1_queue_wait(lam, mu): return _div(lam/mu, mu-lam) if mu>lam and mu else None
def price_variance(std_price, actual_price, actual_qty): return (std_price-actual_price)*actual_qty
def quantity_variance(std_qty, actual_qty, std_price): return (std_qty-actual_qty)*std_price
def target_cost(market_price, required_margin): return market_price-required_margin
def toc_throughput(total_revenue, totally_variable_inputs): return total_revenue-totally_variable_inputs
def toc_net_profit(throughput, operating_expense): return throughput-operating_expense
def toc_roi(throughput, operating_expense, inventory): return _div(throughput-operating_expense, inventory)
def baumol_cash_balance(annual_cash_demand, transaction_fee, interest_rate): return math.sqrt(2*annual_cash_demand*transaction_fee/interest_rate) if interest_rate else None
def miller_orr_target(transaction_fee, variance, daily_rate, lower_limit): return ((3*transaction_fee*variance)/(4*daily_rate))**(1/3)+lower_limit if daily_rate else None
def miller_orr_upper(target, lower_limit): return 3*target-2*lower_limit

def takt_time(available_time, customer_demand): return _div(available_time, customer_demand)
def line_efficiency(task_times): return _div(sum(task_times), len(task_times)*max(task_times)) if task_times else None
def flow_ratio(value_added_time, total_lead_time): return _div(value_added_time, total_lead_time)
def oee(availability, performance, quality): return availability*performance*quality
def dpmo(defects, units, opportunities): return _div(defects*1_000_000, units*opportunities)
def six_sigma_yield(dpmo_value): return 1-dpmo_value/1_000_000
def productivity(output, labor_hours): return _div(output, labor_hours)
def gross_margin(revenue, cogs): return _div(revenue-cogs, revenue)
def operating_margin(operating_income, revenue): return _div(operating_income, revenue)
def net_margin(net_income, revenue): return _div(net_income, revenue)
def ebitda_margin(ebitda, revenue): return _div(ebitda, revenue)
def contribution_margin(price, variable_cost_per_unit): return price-variable_cost_per_unit
def breakeven_units(fixed_costs, price, variable_cost_per_unit): return _div(fixed_costs, price-variable_cost_per_unit)
def dupont_roe(net_margin_v, asset_turnover, equity_multiplier): return net_margin_v*asset_turnover*equity_multiplier

def eoq(annual_demand, order_cost, holding_cost): return math.sqrt(2*annual_demand*order_cost/holding_cost) if holding_cost else None
def reorder_point(daily_demand, lead_time_days, safety_stock=0): return daily_demand*lead_time_days+safety_stock
def inventory_turnover(cogs, avg_inventory): return _div(cogs, avg_inventory)
def days_inventory_outstanding(avg_inventory, cogs): return _div(avg_inventory*365, cogs)
def straight_line_depreciation(cost, salvage, life): return _div(cost-salvage, life)
def declining_balance_depreciation(book_value, rate): return book_value*rate
def sy_d_depreciation(cost, salvage, remaining_life, sum_year_digits): return (cost-salvage)*remaining_life/sum_year_digits

def free_cash_flow(operating_cash_flow, capex): return operating_cash_flow-capex
def fcff(ebit, tax_rate, depreciation, capex, delta_nwc): return ebit*(1-tax_rate)+depreciation-capex-delta_nwc
def fcfe(net_income, depreciation, capex, delta_nwc, net_borrowing): return net_income+depreciation-capex-delta_nwc+net_borrowing
def wacc(equity, debt, cost_equity, cost_debt, tax_rate):
    v=equity+debt; return None if v==0 else equity/v*cost_equity + debt/v*cost_debt*(1-tax_rate)
def eva(nopat, invested_capital, wacc_v): return nopat-invested_capital*wacc_v
def current_ratio(current_assets, current_liabilities): return _div(current_assets, current_liabilities)
def quick_ratio(cash, receivables, marketable_securities, current_liabilities): return _div(cash+receivables+marketable_securities, current_liabilities)
def debt_to_equity(total_debt, equity): return _div(total_debt, equity)
def interest_coverage(ebit, interest_expense): return _div(ebit, interest_expense)
def dscr(operating_income, debt_service): return _div(operating_income, debt_service)
def altman_z(working_capital,total_assets,retained_earnings,ebit,market_value_equity,total_liabilities,sales):
    return 1.2*_div(working_capital,total_assets)+1.4*_div(retained_earnings,total_assets)+3.3*_div(ebit,total_assets)+0.6*_div(market_value_equity,total_liabilities)+1.0*_div(sales,total_assets)
def npv(rate, cashflows): return sum(cf/((1+rate)**i) for i,cf in enumerate(cashflows))
def irr(cashflows, guess=0.1):
    try: return float(np_financial_irr(cashflows))
    except Exception: return None
def np_financial_irr(cashflows):
    # Newton fallback
    r=0.1
    for _ in range(100):
        f=sum(cf/(1+r)**i for i,cf in enumerate(cashflows)); df=sum(-i*cf/(1+r)**(i+1) for i,cf in enumerate(cashflows) if i)
        if abs(df)<1e-12: break
        nr=r-f/df
        if abs(nr-r)<1e-8: return nr
        r=nr
    return r
def payback_period(cashflows):
    cum=0
    for i,cf in enumerate(cashflows):
        prev=cum; cum+=cf
        if cum>=0 and i>0: return i-1 + (-prev/cf if cf else 0)
    return None
def profitability_index(rate, future_cashflows, initial_investment): return _div(sum(cf/((1+rate)**i) for i,cf in enumerate(future_cashflows,1)), abs(initial_investment))
def terminal_value_gordon(fcf_next, wacc_v, growth): return _div(fcf_next, wacc_v-growth)
def enterprise_value(equity_value, debt, cash): return equity_value+debt-cash
def ebitda_multiple_ev(ebitda, multiple): return ebitda*multiple
def eaa(npv_value, rate, n): return npv_value*rate/(1-(1+rate)**(-n)) if rate else _div(npv_value,n)
def capitalized_cost(annual_cost, rate): return _div(annual_cost, rate)

def expected_value(values, probabilities): return sum(v*p for v,p in zip(values, probabilities))
def variance(values, probabilities=None):
    vals=list(map(float, values))
    if probabilities is None: return statistics.pvariance(vals)
    ev=expected_value(vals, probabilities); return sum(p*(v-ev)**2 for v,p in zip(vals, probabilities))
def stddev(values): return statistics.pstdev(list(map(float, values)))
def sharpe_ratio(return_series, risk_free_rate=0):
    vals=pd.Series(return_series).dropna().astype(float); excess=vals-risk_free_rate/len(vals) if len(vals) else vals
    return None if len(excess)<2 or excess.std()==0 else excess.mean()/excess.std()
def sortino_ratio(return_series, target=0):
    vals=pd.Series(return_series).dropna().astype(float); downside=vals[vals<target]
    dd=downside.std(); return None if len(vals)==0 or dd==0 or pd.isna(dd) else (vals.mean()-target)/dd
def value_at_risk(return_series, alpha=0.05): return float(pd.Series(return_series).dropna().quantile(alpha))
def conditional_var(return_series, alpha=0.05):
    vals=pd.Series(return_series).dropna(); var=vals.quantile(alpha); tail=vals[vals<=var]
    return float(tail.mean()) if len(tail) else None
def beta(asset_returns, market_returns):
    a=pd.Series(asset_returns).dropna(); m=pd.Series(market_returns).dropna(); n=min(len(a),len(m));
    return None if n<2 or np.var(m.iloc[-n:])==0 else float(np.cov(a.iloc[-n:], m.iloc[-n:])[0,1]/np.var(m.iloc[-n:]))
def capm_expected_return(rf, beta_v, market_return): return rf+beta_v*(market_return-rf)
def black_scholes_call(S,K,T,r,sigma):
    from math import log,sqrt,exp,erf
    if T<=0 or sigma<=0: return max(S-K,0)
    N=lambda x:0.5*(1+erf(x/math.sqrt(2)))
    d1=(log(S/K)+(r+0.5*sigma*sigma)*T)/(sigma*sqrt(T)); d2=d1-sigma*sqrt(T)
    return S*N(d1)-K*exp(-r*T)*N(d2)
def black_scholes_put(S,K,T,r,sigma):
    from math import log,sqrt,exp,erf
    if T<=0 or sigma<=0: return max(K-S,0)
    N=lambda x:0.5*(1+erf(x/math.sqrt(2)))
    d1=(log(S/K)+(r+0.5*sigma*sigma)*T)/(sigma*sqrt(T)); d2=d1-sigma*sqrt(T)
    return K*exp(-r*T)*N(-d2)-S*N(-d1)
def logistic_probability(beta0, betas, x):
    z=beta0+sum(b*v for b,v in zip(betas,x)); return 1/(1+math.exp(-z))
def hurst_rs(series):
    x=np.array(pd.Series(series).dropna(), dtype=float); n=len(x)
    if n<20: return None
    y=x-x.mean(); z=np.cumsum(y); R=z.max()-z.min(); S=x.std()
    return None if S==0 else math.log(R/S)/math.log(n)
def prospect_value(x, alpha=0.88, beta=0.88, lamb=2.25): return x**alpha if x>=0 else -lamb*((-x)**beta)
def fear_greed(price_momentum, volatility, breadth=0, sentiment=0): return 25*price_momentum - 25*volatility + 25*breadth + 25*sentiment
def kelly_fraction(edge, odds): return _div(edge, odds)
def impermanent_loss(price_ratio): return 2*math.sqrt(price_ratio)/(1+price_ratio)-1

def zscore(x, mean, std): return None if std==0 else (x-mean)/std
def mfcs(fundamental_z, risk_z, physics_z, behavioral_z, weights=(0.35,0.25,0.2,0.2)):
    return sum(w*v for w,v in zip(weights,[fundamental_z,risk_z,physics_z,behavioral_z]))
def signal_from_score(score):
    return "Strong Buy" if score>=1 else "Buy" if score>=0.5 else "Hold" if score>-0.5 else "Sell" if score>-1 else "Strong Sell"
def reverse_dcf_implied_growth(price, fcf0, discount_rate, years=5, terminal_growth=0.03, shares=1, net_debt=0):
    # Bisection on annual FCF growth matching equity price.
    lo, hi = -0.5, 0.8
    target=price*shares+net_debt
    def val(g):
        fcfs=[fcf0*((1+g)**t) for t in range(1,years+1)]
        tv=fcfs[-1]*(1+terminal_growth)/(discount_rate-terminal_growth) if discount_rate>terminal_growth else 0
        return sum(cf/(1+discount_rate)**i for i,cf in enumerate(fcfs,1))+tv/(1+discount_rate)**years
    for _ in range(80):
        mid=(lo+hi)/2
        if val(mid)<target: lo=mid
        else: hi=mid
    return (lo+hi)/2

FORMULA_REGISTRY = {name: obj for name, obj in globals().items() if callable(obj) and not name.startswith('_') and name not in ['pd','np']}
