# Layered System Breakdown

Each layer has a clear responsibility and can be replaced independently as the product grows.

1. Frontend: Streamlit now; React/Next.js later.
2. API: FastAPI contract for integrations.
3. Backend logic: scraping, analytics, ML, reporting, formulas.
4. Database/storage: SQLite local; PostgreSQL/object storage production.
5. Auth/Authz: API token/RBAC now; OIDC later.
6. Hosting/deployment: Podman Compose, systemd, Kubernetes.
7. Cloud compute: VM/containers/Kubernetes/serverless containers.
8. CI/CD/version control: GitHub Actions templates.
9. Role-level security: roles and permission matrix.
10. Rate limiting: app middleware + Nginx; Redis/WAF later.
11. Cache/CDN: TTL cache/Redis/CDN plan.
12. Load balancing/scaling: Nginx/K8s/cloud LB.
13. Error tracking/logging: rotating logs/Sentry/OpenTelemetry plan.
14. Availability/recovery: backups, health checks, runbooks.
