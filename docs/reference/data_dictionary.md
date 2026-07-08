# Data Dictionary

## `market_observations`

| Column | Type | Required | Description | Example |
|---|---|---:|---|---|
| `id` | integer | yes | Surrogate primary key | `1` |
| `date` | text/date | yes | Observation date | `2026-07-08` |
| `source` | text | yes | Data origin | `google_trends`, `bps`, `manual_csv` |
| `category` | text | yes | Business/category grouping | `commodity`, `idx_stock`, `google_trends` |
| `item` | text | yes | Product, keyword, ticker, metric subject | `Beras Premium` |
| `region` | text | no | Region/province/country | `Indonesia`, `Sumatera Selatan` |
| `price` | real | no | Numeric value. Also used for trend index score | `15500`, `87` |
| `volume` | real | no | Optional quantity/volume | `1200000` |
| `metric` | text | no | Meaning of `price` | `price`, `close`, `search_interest` |
| `currency` | text | no | Currency or index unit | `IDR`, `INDEX_0_100` |
| `raw_payload` | text/json | no | Optional raw serialized payload | `{...}` |
| `created_at` | timestamp | yes | Insert/update timestamp | `2026-07-08 10:00:00` |

## `sources`

| Column | Description |
|---|---|
| `id` | Source ID |
| `name` | Unique source name |
| `url` | URL endpoint/page/feed/sitemap |
| `source_type` | `html_table`, `csv_url`, `json_api`, `html_selectors`, `rss_feed`, `sitemap` |
| `table_index` | HTML table index for `html_table` |
| `notes` | Notes or selector JSON for `html_selectors` |
| `active` | Whether batch runner includes the source |
| `created_at` | Created timestamp |

## `scrape_runs`

| Column | Description |
|---|---|
| `id` | Run ID |
| `source_name` | Source name |
| `status` | `success` or `failed` |
| `rows_collected` | Number of normalized rows |
| `raw_csv_path` | Raw artifact path |
| `processed_csv_path` | Processed artifact path |
| `message` | Status/error details |
| `started_at` | Start timestamp |
| `finished_at` | Finish timestamp |
