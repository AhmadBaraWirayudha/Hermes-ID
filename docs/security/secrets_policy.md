# Secrets Policy

## Never commit

- `.env`
- API tokens
- SMTP passwords
- database passwords
- cloud provider keys
- scraping credentials

## Use environment variables

- `INDOMARKET_API_TOKEN`
- `INDOMARKET_SMTP_PASSWORD`
- `DATABASE_URL`
- `REDIS_URL`
- `SENTRY_DSN`

## Production recommendation

Use a managed secret manager:

- AWS Secrets Manager / SSM Parameter Store
- Google Secret Manager
- Azure Key Vault
- Kubernetes Secrets sealed with SealedSecrets or External Secrets Operator

## Rotation

- API tokens: rotate every 90 days.
- SMTP/API provider keys: rotate every 180 days.
- Database passwords: rotate according to organization policy.
