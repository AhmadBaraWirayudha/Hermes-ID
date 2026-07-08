# Production Readiness Checklist

## Application

- [ ] All required folders have README files.
- [ ] `python scripts/validate_project.py` passes.
- [ ] `pytest -q` passes.
- [ ] API OpenAPI exported.
- [ ] Main dashboard starts.
- [ ] API starts.

## Security

- [ ] `.env` is not committed.
- [ ] API token enabled in staging/prod.
- [ ] RBAC reviewed.
- [ ] Secrets stored in secret manager.
- [ ] HTTPS configured.
- [ ] Security scan run.

## Data

- [ ] Sources legally reviewed.
- [ ] Backup strategy configured.
- [ ] Backup restore drill completed.
- [ ] Data quality score monitored.
- [ ] Stale data alert configured.

## Operations

- [ ] Health checks configured.
- [ ] Logs centralized.
- [ ] Sentry or equivalent configured.
- [ ] Prometheus/Grafana configured.
- [ ] Runbooks reviewed.
- [ ] On-call/owner assigned.
