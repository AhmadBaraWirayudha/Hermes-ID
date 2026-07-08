# Database Scripts

Database migration and maintenance helpers.

SQLite to PostgreSQL copy:

```bash
export DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/indomarket
python scripts/db/sqlite_to_postgres.py
```
