# Service Level Objectives

## Starter SLOs

| Service | SLO |
|---|---:|
| API availability | 99.0% monthly |
| Frontend availability | 99.0% monthly |
| Pipeline success | 95% scheduled runs |
| Report generation | 95% under 2 minutes |
| API p95 latency | under 1.5 seconds for cached summary endpoints |

## Error budget

At 99.0% monthly availability, error budget is about 7.2 hours/month.

## Key indicators

- `/health` and `/ready`
- API 5xx rate
- API p95 latency
- pipeline success/failure count
- latest data staleness
- backup age
