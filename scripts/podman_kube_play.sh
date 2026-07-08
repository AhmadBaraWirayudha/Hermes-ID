#!/usr/bin/env bash
set -euo pipefail
podman build -f Containerfile -t localhost/indomarket-insight:latest .
podman kube play infra/podman/kube/indomarket-pod.yaml
