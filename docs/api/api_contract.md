# API Contract

The canonical contract is OpenAPI generated from FastAPI.

Generate:

```bash
python scripts/export_openapi.py
```

Output:

```text
docs/architecture/openapi.json
```

Core paths:

| Method | Path | Permission |
|---|---|---|
| GET | `/health` | public |
| GET | `/ready` | public |
| GET | `/metrics` | public/internal network recommended |
| GET | `/market/summary` | read |
| GET | `/market/quality` | read |
| GET | `/market/latest` | read |
| GET | `/market/observations` | read |
| GET | `/market/alerts` | read |
| GET | `/forecast/{item}` | forecast |
| GET | `/forecast/{item}/backtest` | forecast |
| GET | `/reports/pdf` | report |
| GET | `/reports/tex` | report |

Use `X-API-Token` when API token protection is enabled.
