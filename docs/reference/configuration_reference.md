# Configuration Reference

## `config/settings.json`

Controls app defaults, API token mode, webhook URL, and SMTP notifications.

Template: `config/settings.example.json`

## `config/sources.example.json`

Template for source registry import.

Supported source types:

- `html_table`
- `csv_url`
- `json_api`
- `html_selectors`
- `rss_feed`
- `sitemap`

## `config/alerts.example.json`

Defines monitoring thresholds for stale data, data quality, z-score anomalies, daily changes, and item price bands.

## `config/rbac.example.json`

Defines roles and permissions.

## `config/users.example.json`

Local user-file template. For production, use OIDC/managed identity.

## `config/indonesian_sentiment_lexicon.json`

Simple lexicon for Indonesian/English sentiment scoring.
