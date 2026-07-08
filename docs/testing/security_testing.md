# Security Testing

Recommended checks:

```bash
pip install bandit pip-audit
bandit -r app -c tests/security/bandit.yaml
pip-audit
```

Container image scan options:

```bash
trivy image indomarket-insight:latest
```

Checklist:

- no secrets in git
- `.env` excluded
- API token enabled in staging/prod
- HTTPS at proxy/load balancer
- dependency audit clean or accepted risk documented
