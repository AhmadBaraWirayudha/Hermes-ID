#!/usr/bin/env bash
set -euo pipefail
IMAGE=${1:-localhost/indomarket-insight:latest}
podman build -f Containerfile -t "$IMAGE" .
echo "Built $IMAGE"
if [[ "${PUSH:-0}" == "1" ]]; then
  podman push "$IMAGE"
fi
