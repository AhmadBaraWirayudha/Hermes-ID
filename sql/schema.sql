PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    url TEXT,
    source_type TEXT NOT NULL DEFAULT 'html_table', -- html_table, csv_url, json_api, manual_csv
    table_index INTEGER DEFAULT 0,
    notes TEXT,
    active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS market_observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    source TEXT NOT NULL,
    category TEXT NOT NULL,
    item TEXT NOT NULL,
    region TEXT DEFAULT 'Indonesia',
    price REAL,
    volume REAL,
    metric TEXT DEFAULT 'price',
    currency TEXT DEFAULT 'IDR',
    raw_payload TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date, source, category, item, region, metric)
);

CREATE TABLE IF NOT EXISTS scrape_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name TEXT NOT NULL,
    status TEXT NOT NULL,
    rows_collected INTEGER DEFAULT 0,
    raw_csv_path TEXT,
    processed_csv_path TEXT,
    message TEXT,
    started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    finished_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_obs_date ON market_observations(date);
CREATE INDEX IF NOT EXISTS idx_obs_item ON market_observations(item);
CREATE INDEX IF NOT EXISTS idx_obs_category ON market_observations(category);
CREATE INDEX IF NOT EXISTS idx_obs_region ON market_observations(region);
