# Deployment Checklist

## Before deploy

- [ ] Copy `.env.example` to `.env` and set real values.
- [ ] Set `INDOMARKET_API_TOKEN`.
- [ ] Decide storage backend: SQLite or PostgreSQL.
- [ ] Configure backup location.
- [ ] Review scraper sources and legal permissions.
- [ ] Run tests: `make test`.
- [ ] Build OCI image.

## Podman Compose production

```bash
cp .env.example .env
podman-compose -f podman-compose.prod.yml up --build -d
python scripts/healthcheck.py http://localhost/api/health http://localhost/_stcore/health
```

## Post-deploy

- [ ] Create first backup.
- [ ] Generate first report.
- [ ] Test API token.
- [ ] Test alert pipeline.
- [ ] Set cron/systemd timer.
- [ ] Configure monitoring.
