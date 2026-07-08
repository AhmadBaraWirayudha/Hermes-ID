import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

import pandas as pd
from business_models import revenue_core, roas, hhi
from quality import data_quality_report
from utils import normalize_market_df


def test_business_models():
    assert revenue_core(10, 15000) == 150000
    assert roas(200000, 50000) == 4
    assert hhi([40, 30, 20, 10]) == 3000


def test_quality_and_normalize():
    raw = pd.DataFrame({"tanggal": ["2026-07-07"], "produk": ["Beras"], "harga": ["15.000"], "provinsi": ["Sumsel"]})
    clean = normalize_market_df(raw, source="test", default_category="commodity")
    report = data_quality_report(clean)
    assert report["rows"] == 1
    assert report["score"] > 70
from holy_grail_formulas import FORMULA_REGISTRY, npv, black_scholes_call, mfcs
from timeframes import apply_timeframe


def test_holy_grail_registry():
    assert len(FORMULA_REGISTRY) > 80
    assert round(npv(0.1, [-100, 60, 60]), 2) == 4.13
    assert black_scholes_call(100, 100, 1, 0.05, 0.2) > 0
    assert mfcs(1, 0, 0, 0) == 0.35


def test_timeframes():
    df = pd.DataFrame({
        "date": pd.date_range("2025-01-01", periods=20, freq="D"),
        "source": "x", "category": "c", "item": "i", "region": "ID",
        "metric": "price", "currency": "IDR", "price": range(20), "volume": 1
    })
    out = apply_timeframe(df, "All", "Weekly")
    assert len(out) < len(df)
from alerts import evaluate_alerts
from scenario import monte_carlo_price_paths, summarize_paths, dcf_scenario


def test_alerts_and_scenario():
    df = pd.DataFrame({
        "date": pd.date_range("2026-01-01", periods=40, freq="D"),
        "source": "x", "category": "c", "item": "i", "region": "ID",
        "metric": "price", "currency": "IDR", "price": list(range(100, 140)), "volume": 1
    })
    alerts = evaluate_alerts(df)
    assert len(alerts) >= 1
    paths = monte_carlo_price_paths(100, days=10, simulations=20)
    summary = summarize_paths(paths)
    assert summary["simulations"] == 20
    scen = dcf_scenario(100, [0.0, 0.1], 0.12, 0.03)
    assert len(scen) == 2
from settings import load_settings
from catalog import database_catalog


def test_settings_and_catalog():
    settings = load_settings()
    assert "default_region" in settings
    cat = database_catalog()
    assert hasattr(cat, "columns")
from data_studio import growth_metrics, rebase_index, pivot_market
from sentiment import score_text, analyze_observation_text
from scheduler_helper import cron_line


def test_data_studio_sentiment_scheduler():
    df = pd.DataFrame({
        "date": pd.date_range("2026-01-01", periods=10, freq="D"),
        "source": "x", "category": "c", "item": "harga naik", "region": "ID",
        "metric": "price", "currency": "IDR", "price": range(10, 20), "volume": 1
    })
    assert "dod_pct" in growth_metrics(df).columns
    assert "index_rebased" in rebase_index(df).columns
    assert not pivot_market(df).empty
    assert score_text("harga naik dan menguat")["sentiment_label"] == "positive"
    assert "sentiment_label" in analyze_observation_text(df).columns
    assert "pipeline.py" in cron_line()
from security import hash_password, verify_password, user_has_permission
from cache_layer import ttl_cache, clear_cache


def test_security_and_cache_layer():
    encoded = hash_password("secret")
    assert verify_password("secret", encoded)
    assert not verify_password("wrong", encoded)
    assert user_has_permission({"roles": ["admin"]}, "anything")
    clear_cache()
    calls = {"n": 0}
    @ttl_cache(seconds=10)
    def f(x):
        calls["n"] += 1
        return x * 2
    assert f(2) == 4 and f(2) == 4
    assert calls["n"] == 1
from storage_layer import storage_backend_name, object_storage_config
from redis_cache import cache_set, cache_get, cache_delete


def test_storage_and_redis_cache_fallback():
    assert storage_backend_name() in ["sqlite", "postgresql"]
    assert "provider" in object_storage_config()
    cache_set("x", {"a": 1}, ttl=5)
    assert cache_get("x")["a"] == 1
    cache_delete("x")
    assert cache_get("x") is None
from repositories.observations_repo import list_observations
from services.market_service import get_market_summary


def test_repository_service_layers():
    df = list_observations(limit=5)
    assert hasattr(df, "columns")
    summary = get_market_summary()
    assert "rows" in summary
from domain.entities import MarketObservation
from schemas.market import MarketObservationOut
from object_storage import get_object_uri


def test_domain_schema_object_storage():
    obs = MarketObservation(date="2026-01-01", source="test", category="c", item="i", price=1.0)
    assert obs.region == "Indonesia"
    dto = MarketObservationOut(date=obs.date, source=obs.source, category=obs.category, item=obs.item, price=obs.price)
    assert dto.currency == "IDR"
    assert "x.txt" in get_object_uri("x.txt")
