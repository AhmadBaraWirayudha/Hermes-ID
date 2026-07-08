# Real-Time Signal Engine

The real-time signal engine converts OSINT events and tension indicators into scored signals.

## Inputs

- OSINT RSS events
- permitted web page events
- approved social media CSV imports
- Pentagon Pizza Index and DEFCON-style tension indicators
- watchlist rules

## Outputs

Stored in SQLite table:

```text
realtime_signals
```

Fields include:

```text
observed_at
signal_type
source
category
title
url
score
severity
reason
payload
```

## Severity scoring

| Score | Severity |
|---|---|
| 8 or higher | critical |
| 5 to 7.99 | high |
| 3 to 4.99 | medium |
| 1 to 2.99 | low |
| below 1 | info |

## Watchlist

Rules are configured in:

```text
config/realtime_watchlist.json
```

Each rule includes:

```text
name
pattern
category
severity_weight
active
notes
```

Patterns are treated as regular expressions when possible.

## Run every five minutes

```bash
python scripts/run_realtime_monitor.py --interval 300
```

## API endpoints

```text
GET  /realtime/status
POST /realtime/run-cycle
GET  /realtime/signals
GET  /realtime/runs
GET  /realtime/watchlist
POST /realtime/seed-watchlist
POST /realtime/export-signals
```
