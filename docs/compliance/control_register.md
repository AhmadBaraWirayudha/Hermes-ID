# Compliance Control Register

| Control ID | Control | Owner | Evidence | Frequency | Status |
|---|---|---|---|---|---|
| GOV-001 | Maintain compliance register and legal domain map | Compliance owner | docs/compliance | Quarterly | Draft |
| GOV-002 | Review business model for licensing implications | Founder and counsel | Legal memo | Before launch and product changes | Required |
| DATA-001 | Maintain data dictionary and source lineage | Data owner | docs/reference/data_dictionary.md and data catalog | Monthly | Implemented |
| DATA-002 | Review data source rights and terms | Data owner | source onboarding checklist | Per source | Required |
| PRIV-001 | Map personal data processing activities | Privacy owner | data processing register | Quarterly | Required |
| PRIV-002 | Implement data subject rights workflow | Privacy owner | privacy operations procedure | Before user accounts | Planned |
| SEC-001 | Enforce API authentication in staging and production | Security owner | settings and API tests | Per release | Implemented as token option |
| SEC-002 | Rotate API and SMTP secrets | Security owner | secret rotation log | 90 to 180 days | Planned |
| SEC-003 | Run dependency and security checks | Engineering | audit outputs | Per release | Implemented as scripts |
| OPS-001 | Run backup restore drill | Operations | runbook evidence | Monthly | Implemented as docs/scripts |
| OPS-002 | Monitor health endpoints | Operations | monitoring dashboard | Continuous | Implemented as endpoints |
| MODEL-001 | Register trained models and metrics | ML owner | model registry | Per model | Implemented |
| MODEL-002 | Backtest forecasting models | ML owner | backtest CSV and metrics | Per model release | Implemented |
| AI-001 | Review AI outputs for explainability and disclaimers | ML owner | model card | Per model release | Planned |
| MKT-001 | Review marketing claims for misleading statements | Marketing and compliance | campaign approval record | Per campaign | Required |
| GEO-001 | Maintain geopolitical risk register | Strategy owner | docs/geopolitics | Monthly | Draft |
| INC-001 | Maintain incident response runbook | Operations | docs/runbooks | Quarterly | Implemented |
