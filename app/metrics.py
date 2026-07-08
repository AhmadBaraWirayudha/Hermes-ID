"""Prometheus metrics integration with graceful fallback."""
try:
    from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
except Exception:  # fallback when prometheus_client not installed yet
    Counter = Histogram = Gauge = None
    CONTENT_TYPE_LATEST = "text/plain"
    def generate_latest(): return b"prometheus_client_not_installed 1\n"

if Counter:
    API_REQUESTS = Counter("indomarket_api_requests_total", "API requests", ["path", "method", "status"])
    API_LATENCY = Histogram("indomarket_api_request_seconds", "API request latency", ["path", "method"])
    OBS_ROWS = Gauge("indomarket_observation_rows", "Number of market observation rows")
else:
    API_REQUESTS = API_LATENCY = OBS_ROWS = None
