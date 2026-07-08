#!/usr/bin/env bash
set -euo pipefail
if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env from .env.example. Review secrets before production use."
fi
podman-compose -f podman-compose.prod.yml up --build -d
python scripts/healthcheck.py http://localhost/api/health http://localhost/_stcore/health || true
