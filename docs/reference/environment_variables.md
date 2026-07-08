# Environment Variable Reference

| Variable | Required | Default | Description |
|---|---:|---|---|
| `TZ` | no | `Asia/Jakarta` | Runtime timezone |
| `DATABASE_URL` | no | SQLite | SQLAlchemy database URL for production DB |
| `REDIS_URL` | no | empty | Redis URL for distributed cache/queue |
| `INDOMARKET_API_TOKEN` | if API token enabled | empty | API token used with `X-API-Token` |
| `INDOMARKET_SMTP_PASSWORD` | if SMTP enabled | empty | SMTP password |
| `SENTRY_DSN` | no | empty | Sentry error tracking DSN |
| `SENTRY_TRACES_SAMPLE_RATE` | no | `0.05` | Sentry trace sampling |
| `ENVIRONMENT` | no | `development` | Environment name |
| `OBJECT_STORAGE_PROVIDER` | no | `local` | `local`, `s3`, or `minio` |
| `OBJECT_STORAGE_BUCKET` | for s3/minio | empty | Bucket name |
| `OBJECT_STORAGE_ENDPOINT_URL` | minio/custom | empty | S3-compatible endpoint URL |
| `OBJECT_STORAGE_REGION` | s3 | empty | Cloud object-storage region |
| `OBJECT_STORAGE_LOCAL_ROOT` | no | `data` | Local fallback object storage root |
