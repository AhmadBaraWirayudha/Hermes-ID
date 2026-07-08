#!/usr/bin/env bash
set -euo pipefail
# Safe chaos drill for local Podman Compose: restart API and verify recovery.
COMPOSE=${COMPOSE_FILE:-podman-compose.prod.yml}
echo "Restarting API container..."
podman-compose -f "$COMPOSE" restart api
sleep 10
python scripts/healthcheck.py http://localhost/api/health
echo "Chaos drill passed: API recovered."
