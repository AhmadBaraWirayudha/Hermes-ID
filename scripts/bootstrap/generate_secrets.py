import secrets
print("INDOMARKET_API_TOKEN=" + secrets.token_urlsafe(48))
print("MINIO_ROOT_PASSWORD=" + secrets.token_urlsafe(32))
print("GRAFANA_ADMIN_PASSWORD=" + secrets.token_urlsafe(24))
