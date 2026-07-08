# Compliance Operating Model

## Roles

| Role | Responsibility |
|---|---|
| Founder or product owner | Owns business model, risk appetite, and final go-live decisions |
| Compliance owner | Maintains legal register, policy set, and regulator engagement tracker |
| Data owner | Owns source approvals, data quality, lineage, and retention |
| Security owner | Owns access control, secrets, logging, incident response, and vulnerability management |
| ML owner | Owns model validation, backtesting, model registry, and model risk documentation |
| Operations owner | Owns backup, recovery, availability, and monitoring |

## Compliance cadence

| Activity | Frequency |
|---|---|
| Source rights review | Before adding a source |
| Data quality review | Weekly or per ingestion run |
| Security dependency review | Per release |
| Backup restore drill | Monthly |
| Model backtest review | Per model release |
| Geopolitical risk review | Monthly or event-driven |
| Legal perimeter review | Before launch and before new regulated features |

## Three lines of defense model

1. Product and engineering operate controls.
2. Compliance and risk review controls.
3. Independent legal, audit, or external advisor validates high-risk areas.
