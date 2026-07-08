#!/usr/bin/env bash
set -euo pipefail
mkdir -p wheelhouse
python -m pip download -r requirements.txt -d wheelhouse
tar -czf wheelhouse.tar.gz wheelhouse requirements.txt
echo "Created wheelhouse.tar.gz"
