#!/usr/bin/env bash
set -euo pipefail
podman system prune -f
podman volume prune -f || true
