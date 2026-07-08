# Scaling Playbook

## Stage 1: Local MVP

- SQLite
- Streamlit only
- Manual scraping/import

## Stage 2: Single VM production

- Podman Compose with frontend + API + Nginx
- SQLite or PostgreSQL
- Scheduled pipeline
- Backups

## Stage 3: Team production

- Managed PostgreSQL
- Redis cache/queue
- Object storage for raw/processed artifacts
- Separate workers for scraping/reporting
- Central logs/Sentry

## Stage 4: High scale

- Kubernetes or managed containers
- Horizontal replicas
- API Gateway/WAF
- CDN for static/report delivery
- Queue-driven scraping and ML
- Multi-zone DB backups/replicas

## Bottlenecks and fixes

| Bottleneck | Fix |
|---|---|
| SQLite write lock | PostgreSQL |
| Slow scraping | background workers + queue |
| Slow reports | async tasks + object storage |
| Repeated API reads | Redis cache |
| Single VM failure | replicas + managed DB |
