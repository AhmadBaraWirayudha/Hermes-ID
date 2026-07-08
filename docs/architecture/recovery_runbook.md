# Availability and Recovery Runbook

## Health checks

- Frontend: `http://HOST/_stcore/health`
- API: `http://HOST/api/health` or direct `http://HOST:8000/health`

## Backup

```bash
python app/cli.py backup-db
python app/cli.py backup-workspace
```

## Restore SQLite

```bash
python app/cli.py restore-db backups/YYYYMMDD_HHMMSS_indomarket.sqlite.bak
```

## RPO/RTO starter targets

| Tier | RPO | RTO |
|---|---:|---:|
| Local MVP | 24h | 4h |
| Small production | 1h | 1h |
| Critical production | 5-15m | 15-30m |

## Incident checklist

1. Check `/health` endpoints.
2. Check container/service status.
3. Review `logs/indomarket.log`.
4. Restore latest DB backup if data corruption occurred.
5. Re-run pipeline: `python app/pipeline.py --alerts --export --report both`.
6. Document incident and prevention action.
