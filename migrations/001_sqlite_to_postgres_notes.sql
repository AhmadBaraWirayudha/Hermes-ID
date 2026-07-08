-- Migration notes for moving from SQLite MVP to PostgreSQL production.
-- 1. Create PostgreSQL DB.
-- 2. Set DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/indomarket
-- 3. Recreate schema with compatible types.
-- 4. Export SQLite tables to CSV and COPY into PostgreSQL.

CREATE TABLE IF NOT EXISTS sources (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    url TEXT,
    source_type TEXT NOT NULL DEFAULT 'html_table',
    table_index INTEGER DEFAULT 0,
    notes TEXT,
    active INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS market_observations (
    id BIGSERIAL PRIMARY KEY,
    date TEXT NOT NULL,
    source TEXT NOT NULL,
    category TEXT NOT NULL,
    item TEXT NOT NULL,
    region TEXT DEFAULT 'Indonesia',
    price DOUBLE PRECISION,
    volume DOUBLE PRECISION,
    metric TEXT DEFAULT 'price',
    currency TEXT DEFAULT 'IDR',
    raw_payload TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(date, source, category, item, region, metric)
);
