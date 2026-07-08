# SQLite to PostgreSQL Migration

## 1. Provision PostgreSQL

Use a managed PostgreSQL service or self-hosted PostgreSQL.

## 2. Set DATABASE_URL

```bash
export DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/indomarket
```

## 3. Create schema

Use Alembic:

```bash
alembic upgrade head
```

Or manually adapt `migrations/001_sqlite_to_postgres_notes.sql`.

## 4. Copy data

```bash
python scripts/db/sqlite_to_postgres.py
```

## 5. Verify counts

Compare SQLite and PostgreSQL row counts before switching traffic.

## 6. Switch app config

Set `DATABASE_URL` in your `.env` or secret manager.
