# Real-Time OSINT Monitoring

Hermes Analytics ID includes a compliant real-time monitoring layer for public news, RSS feeds, approved web pages, social media imports, and Pentagon Pizza Index style tension indicators.

## Compliance rules

- Prefer official APIs, RSS feeds, and downloadable datasets.
- Respect robots.txt and source terms.
- Do not bypass paywalls, logins, CAPTCHAs, rate limits, or access controls.
- Social media data should use official APIs, approved exports, or user-owned CSV files.
- Do not collect personal data unless approved by privacy review.

## Five-minute automatic run

```bash
python scripts/run_realtime_monitor.py --interval 300
```

Windows:

```text
START_REALTIME_MONITOR_WINDOWS.cmd
```

Linux:

```bash
./START_REALTIME_MONITOR_LINUX.sh
```

## One-time run

```bash
python scripts/run_realtime_monitor.py --once
```

## API endpoints

```text
GET  /osint/events
GET  /osint/runs
GET  /osint/sources
POST /osint/seed-sources
POST /osint/run-cycle
POST /osint/pentagon-pizza-index
GET  /osint/tension-indicators
```

## Pentagon Pizza Index monitor

The monitor fetches the public page at `https://www.defconlevel.com/` and attempts to extract summary snippets related to Pentagon Pizza Index, DEFCON, threat, and tension terms. Extraction is best-effort because page structure may change.

## Indonesian news sources

Default source examples are in:

```text
config/osint_sources.example.json
```

Verify each source's terms before production activation.

## Real-time signal scoring

See:

```text
docs/osint/realtime_signal_engine.md
```

The signal engine adds watchlist scoring, severity labels, signal storage, and `/realtime` API endpoints.
