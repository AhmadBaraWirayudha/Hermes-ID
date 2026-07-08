# ADR-0002: API Router + Service + Repository Pattern

## Status
Accepted

## Decision
Split new API/backend code into:

- `api_routers/`: HTTP concerns.
- `services/`: business use-cases.
- `repositories/`: data access.

## Consequences

- Easier testing.
- Easier migration from SQLite to PostgreSQL.
- API routes stay thin.
