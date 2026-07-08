# Threat Model

## Assets

- Market observations database.
- Raw/processed CSV/XLSX/PDF/Parquet reports.
- Scraper source registry.
- API token and SMTP credentials.
- Model artifacts.

## Main threats and controls

| Threat | Control |
|---|---|
| Unauthorized API access | API token, RBAC, HTTPS at proxy/LB |
| Excessive scraping/API abuse | rate limits, delays, robots check, WAF/API gateway |
| Credential leak | env variables, no secrets in git, `.env.example` only |
| Data corruption | backups, manifests, restore runbook |
| Dependency vulnerabilities | CI, pinned requirements policy, periodic upgrades |
| Scraping legal/ToS violations | source review, robots, official APIs preferred |
| Report leakage | role-based downloads, object storage signed URLs in production |
| Single instance failure | health checks, replicas, managed DB backups |

## Security upgrade path

1. Enforce HTTPS with cloud load balancer.
2. Replace token auth with OIDC/JWT.
3. Move secrets to cloud secret manager.
4. Replace SQLite with managed PostgreSQL.
5. Centralize logs and enable Sentry.
6. Add WAF and distributed Redis rate limiting.
