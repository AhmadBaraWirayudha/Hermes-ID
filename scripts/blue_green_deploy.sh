#!/usr/bin/env bash
set -euo pipefail
# Minimal blue/green deployment helper using Podman Compose project names.
# Usage: ./scripts/blue_green_deploy.sh blue|green
TARGET=${1:-green}
if [[ "$TARGET" != "blue" && "$TARGET" != "green" ]]; then
  echo "Usage: $0 blue|green" >&2; exit 1
fi
export COMPOSE_PROJECT_NAME="indomarket_${TARGET}"
podman-compose -f podman-compose.prod.yml up --build -d
sleep 10
python scripts/healthcheck.py "http://localhost/api/health" || { echo "Healthcheck failed"; exit 1; }
echo "${TARGET} deployment healthy. Update load balancer/upstream to point to this stack."
