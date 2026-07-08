"""FastAPI service for IndoMarket Insight."""
import time
from fastapi import FastAPI, Request, Depends
from fastapi.responses import Response
from db import init_db, load_observations
from security import rate_limit, require_api_auth
from cache_layer import ttl_cache
from observability import LOGGER, setup_sentry_if_configured
from metrics import API_REQUESTS, API_LATENCY, OBS_ROWS, generate_latest, CONTENT_TYPE_LATEST
from services.market_service import get_market_summary, get_quality_report, get_alert_records
from api_routers.market import router as market_router
from api_routers.forecast import router as forecast_router
from api_routers.reports import router as reports_router
from api_routers.osint import router as osint_router
from api_routers.realtime import router as realtime_router

api = FastAPI(title="IndoMarket Insight API", version="0.13.0")
setup_sentry_if_configured()
api.include_router(market_router)
api.include_router(forecast_router)
api.include_router(reports_router)
api.include_router(osint_router)
api.include_router(realtime_router)

@api.middleware("http")
async def observability_middleware(request: Request, call_next):
    rate_limit(request, limit=120, window_seconds=60)
    start = time.time()
    response = None
    try:
        response = await call_next(request)
        return response
    finally:
        elapsed = time.time() - start
        status = str(response.status_code) if response else "500"
        path = request.url.path
        LOGGER.info("api_request path=%s method=%s status=%s elapsed=%.4f", path, request.method, status, elapsed)
        if API_REQUESTS:
            API_REQUESTS.labels(path=path, method=request.method, status=status).inc()
            API_LATENCY.labels(path=path, method=request.method).observe(elapsed)

@api.on_event("startup")
def _startup():
    init_db()

@ttl_cache(seconds=20)
def _cached_summary():
    return get_market_summary()

@ttl_cache(seconds=20)
def _cached_quality():
    return get_quality_report()

@api.get("/health")
def health():
    return {"status": "ok", "service": "indomarket-api"}

@api.get("/ready")
def ready():
    df = load_observations()
    if OBS_ROWS:
        OBS_ROWS.set(len(df))
    return {"status": "ready", "rows": len(df)}

@api.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# Backward-compatible top-level endpoints
@api.get("/summary")
def summary(_: dict = Depends(require_api_auth("read"))):
    return _cached_summary()

@api.get("/quality")
def quality(_: dict = Depends(require_api_auth("read"))):
    return _cached_quality()

@api.get("/alerts")
def alerts(_: dict = Depends(require_api_auth("read"))):
    return get_alert_records().to_dict(orient="records")
