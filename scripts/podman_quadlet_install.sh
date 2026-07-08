#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
mkdir -p ~/.config/containers/systemd
cp "$ROOT"/infra/podman/quadlet/* ~/.config/containers/systemd/
systemctl --user daemon-reload
podman build -f "$ROOT/Containerfile" -t localhost/indomarket-insight:latest "$ROOT"
systemctl --user enable --now indomarket-frontend.service indomarket-api.service || true
loginctl enable-linger "$USER" || true
echo "Quadlet install attempted. Check: systemctl --user status indomarket-api indomarket-frontend"
