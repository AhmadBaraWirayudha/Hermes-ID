#!/usr/bin/env bash
set -euo pipefail
if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y podman python3-pip
elif command -v dnf >/dev/null 2>&1; then
  sudo dnf install -y podman python3-pip
fi
python3 -m pip install --user podman-compose
echo "Podman install complete. Run: ./scripts/podman_run_prod.sh"
