"""Service layer for market intelligence operations."""
from analytics import kpi_summary, add_market_features, correlation_matrix
from quality import data_quality_report
from alerts import evaluate_alerts
from repositories.observations_repo import list_observations, latest_observations


def get_market_summary():
    return kpi_summary(list_observations(limit=10_000_000))


def get_quality_report():
    return data_quality_report(list_observations(limit=10_000_000))


def get_latest_records():
    return latest_observations()


def get_alert_records(rules=None):
    return evaluate_alerts(list_observations(limit=10_000_000), rules)


def get_featured_market_data(limit=5000):
    return add_market_features(list_observations(limit=limit))
