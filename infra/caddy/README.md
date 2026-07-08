# Caddy Reverse Proxy

Caddy is a free/open-source reverse proxy with automatic HTTPS support.

Local HTTP example:

```bash
caddy run --config infra/caddy/Caddyfile
```

For a real domain, replace `:80` in the Caddyfile with your domain name:

```text
indomarket.example.com {
  handle_path /api/* { reverse_proxy localhost:8000 }
  handle { reverse_proxy localhost:8501 }
}
```

Caddy can be used instead of Nginx if you prefer automatic TLS.
