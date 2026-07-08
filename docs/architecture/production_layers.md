# IndoMarket Insight Production Layered Architecture

This document maps the app into the production layers you requested.

## 1. Frontend Layer

**Current implementation**

- Streamlit UI: `app/main.py`
- Pages: Overview, Sources, Google Trends, CSV Import, Data Quality, Alerts, Data Catalog, Data Studio, Sentiment, Analytics, Scenario Lab, Business Models, Holy Grail Formulas, Forecast ML, Backtest, Model Registry, SQL, Exports, Settings & Backup.

**Production deployment**

- Run as `frontend` container on port `8501`.
- Reverse proxied by Nginx or cloud load balancer.
- Static assets can be served through CDN if frontend is later migrated to React/Next.js.

## 2. API Layer

**Current implementation**

- FastAPI service: `app/api.py`
- Endpoints:
  - `/health`
  - `/summary`
  - `/quality`
  - `/observations`
  - `/alerts`
  - `/forecast/{item}`
  - `/report/pdf`
  - `/report/tex`

**Production deployment**

- Run as `api` container on port `8000`.
- Nginx routes `/api/*` to the API.
- Optional token auth through `X-API-Token`.

## 3. Backend Logic Layer

**Modules**

- Scraping: `scraper.py`, `scraping_ext.py`, `google_trends.py`
- Analytics: `analytics.py`, `data_studio.py`, `scenario.py`
- ML: `ml.py`, `backtesting.py`, `model_registry.py`
- Business formulas: `business_models.py`, `holy_grail_formulas.py`
- Reporting: `reporting.py`, `exporter.py`
- Automation: `pipeline.py`, `batch_runner.py`, `scheduler_helper.py`

## 4. Database and Storage Layer

**Current implementation**

- SQLite database: `data/indomarket.sqlite`
- Raw storage: `data/raw/`
- Processed storage: `data/processed/`
- Models: `models/`
- Backups: `backups/`

**Production path**

- MVP/local: SQLite.
- Team/production: PostgreSQL for relational observations and S3/GCS/Azure Blob for raw/processed objects.
- Parquet exports supported for data lake workflows.

## 5. Authentication and Authorization Layer

**Current implementation**

- API token auth: `settings.api_token_enabled` + `INDOMARKET_API_TOKEN`.
- RBAC helpers: `app/security.py`.
- RBAC config: `config/rbac.example.json`.
- User file template: `config/users.example.json`.

**Recommended production upgrade**

- Use managed identity provider: Auth0, Keycloak, AWS Cognito, Azure AD, or Google Identity Platform.
- Use OIDC/JWT and map groups to roles.

## 6. Hosting and Deployment Layer

**Included**

- Containerfile
- `podman-compose.yml`
- `podman-compose.prod.yml`
- Nginx config: `infra/nginx/nginx.conf`
- Systemd units: `infra/systemd/`
- Kubernetes skeleton: `infra/kubernetes/`

**Suggested hosting options**

- Single VM: Podman Compose + Nginx.
- Managed containers: Cloud Run, ECS/Fargate, Azure Container Apps.
- Kubernetes: GKE/EKS/AKS.

## 7. Cloud Compute Layer

**Small deployment**

- 1 VM, 2 vCPU, 4-8 GB RAM.
- Podman Compose.

**Growing deployment**

- Separate frontend/API workers.
- Managed PostgreSQL.
- Object storage.
- Redis cache.
- Queue workers for scraping and ML.

## 8. CI/CD and Version Control Layer

**Included**

- GitHub Actions compile/test workflow: `.github/workflows/ci.yml`
- Docker build CI/CD template: `.github/workflows/docker-ci-cd.yml`

**Recommended version strategy**

- `main`: production-ready.
- `develop`: integration.
- feature branches: `feature/google-trends`, `feature/rbac`, etc.
- semantic versioning: `vMAJOR.MINOR.PATCH`.

## 9. Role-Level Security Layer

**Roles**

- `admin`: all permissions.
- `analyst`: read, forecast, report, export.
- `operator`: read, scrape, export.
- `viewer`: read only.

**Permissions**

- `read`
- `scrape`
- `forecast`
- `report`
- `export`
- `*`

## 10. Rate Limiting Layer

**Current implementation**

- In-memory API rate limiter: `security.rate_limit`.
- Nginx rate limiting in `infra/nginx/nginx.conf`.

**Production upgrade**

- Redis-backed distributed rate limiter.
- API Gateway / Cloud Armor / AWS WAF.

## 11. Cache and CDN Layer

**Current implementation**

- Tiny TTL cache: `app/cache_layer.py` for API summary/quality endpoints.

**Production upgrade**

- Redis for API/backend cache.
- CDN for static files/reports/downloads.
- Object storage signed URLs for generated reports.

## 12. Load Balancer and Scaling Layer

**Included**

- Nginx reverse proxy for local Podman Compose.
- Kubernetes Deployment replicas and Ingress skeleton.

**Production upgrade**

- Cloud Load Balancer.
- Horizontal Pod Autoscaler.
- Separate workers for scraping/ML/report generation.

## 13. Error Tracking and Logging Layer

**Current implementation**

- Rotating logs: `logs/indomarket.log`.
- Observability helper: `app/observability.py`.
- Optional Sentry via `SENTRY_DSN`.

**Production upgrade**

- Sentry for exceptions.
- OpenTelemetry traces.
- Centralized logs: CloudWatch, GCP Logging, Azure Monitor, ELK, Grafana Loki.

## 14. Availability and Recovery Layer

**Current implementation**

- SQLite backup/restore: `app/backup.py`.
- Workspace ZIP backup.
- Pipeline automation.
- Health endpoints.

**Production upgrade**

- Managed DB automated backups.
- Object storage versioning.
- Multi-zone deployment.
- Disaster recovery runbook.
- RPO/RTO definitions.

## Recommended production topology

```text
Internet
  |
CDN / WAF
  |
Cloud Load Balancer
  |
Nginx / Ingress
  |------------------------|
Frontend Streamlit        FastAPI API
  |                        |
  |                        Backend services / workers
  |                        |
  |--------------|---------|--------------|
PostgreSQL      Redis Cache/Queue      Object Storage
  |
Backups / PITR / Replication
```

## Layer-to-file map

| Layer | Files |
|---|---|
| Frontend | `app/main.py` |
| API | `app/api.py` |
| Backend logic | `app/*.py` analytical/scraper/model modules |
| Database/storage | `app/db.py`, `sql/schema.sql`, `data/` |
| Auth/RBAC | `app/security.py`, `config/rbac.example.json`, `config/users.example.json` |
| Deployment | `Containerfile`, `podman-compose.prod.yml`, `infra/` |
| Cloud compute | `infra/kubernetes/`, compose/systemd templates |
| CI/CD | `.github/workflows/` |
| Rate limiting | `app/security.py`, `infra/nginx/nginx.conf` |
| Cache/CDN | `app/cache_layer.py`, Nginx/CDN guidance |
| Load balancing/scaling | Nginx, K8s manifests |
| Error/logging | `app/observability.py`, `logs/` |
| Availability/recovery | `app/backup.py`, `app/pipeline.py`, backups |
```
