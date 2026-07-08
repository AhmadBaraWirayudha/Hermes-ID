"""Lightweight IndoMarket Insight API client."""
from __future__ import annotations
import requests

class IndoMarketClient:
    def __init__(self, base_url="http://localhost/api", token: str | None = None, timeout=30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        if token:
            self.session.headers.update({"X-API-Token": token})

    def _get(self, path, **params):
        r = self.session.get(f"{self.base_url}{path}", params={k:v for k,v in params.items() if v is not None}, timeout=self.timeout)
        r.raise_for_status()
        ctype = r.headers.get("content-type", "")
        if "application/json" in ctype:
            return r.json()
        return r.content

    def health(self):
        return self._get("/health")

    def ready(self):
        return self._get("/ready")

    def summary(self):
        return self._get("/market/summary")

    def quality(self):
        return self._get("/market/quality")

    def latest(self):
        return self._get("/market/latest")

    def observations(self, limit=500, item=None, region=None, category=None):
        return self._get("/market/observations", limit=limit, item=item, region=region, category=category)

    def alerts(self):
        return self._get("/market/alerts")

    def forecast(self, item, horizon=14, region=None):
        return self._get(f"/forecast/{item}", horizon=horizon, region=region)

    def backtest(self, item, horizon=7, min_train=45, step=7, region=None):
        return self._get(f"/forecast/{item}/backtest", horizon=horizon, min_train=min_train, step=step, region=region)

    def report_pdf(self, out_path="indomarket_report.pdf"):
        data = self._get("/reports/pdf")
        with open(out_path, "wb") as f:
            f.write(data)
        return out_path

    def report_tex(self, out_path="indomarket_report.tex"):
        data = self._get("/reports/tex")
        with open(out_path, "wb") as f:
            f.write(data)
        return out_path
