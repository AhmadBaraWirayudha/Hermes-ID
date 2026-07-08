# Load Testing

Install k6:

```bash
# macOS
brew install k6
# Windows
winget install k6.k6
```

Run smoke load test:

```bash
BASE_URL=http://localhost/api k6 run tests/load/k6_api_smoke.js
```

Starter thresholds:

- error rate below 5%
- p95 latency below 1500ms

Scale test gradually: 5 VUs -> 25 -> 100.
