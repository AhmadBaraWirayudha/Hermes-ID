# ADR-0003: Prometheus Metrics

## Status
Accepted

## Decision
Expose `/metrics` in FastAPI and provide Prometheus/Grafana configs.

## Consequences

- Local production stack can observe API request count/latency.
- Cloud deployments can scrape metrics with managed Prometheus.
