# Cloud Cost Model Starter

Approximate monthly components:

| Component | Small | Team | Scale |
|---|---:|---:|---:|
| Compute containers/VMs | 1 small VM | 2-4 containers | autoscaled nodes |
| Database | SQLite/free | managed Postgres small | HA Postgres |
| Object storage | low | low/medium | medium |
| Redis | optional | small managed Redis | HA Redis |
| Monitoring | free tier | managed metrics | full observability |
| CDN/WAF | optional | recommended | required |

Cost drivers:

- scraping frequency
- report generation volume
- ML training frequency
- stored raw artifacts
- dashboard/API traffic

Optimization:

- cache expensive endpoints
- batch scrapes
- store raw archives in lifecycle-managed object storage
- move long jobs to scheduled workers
