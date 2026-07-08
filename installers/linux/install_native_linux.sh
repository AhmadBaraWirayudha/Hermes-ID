#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
cd "$ROOT"
if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y python3-venv python3-pip g++ curl
elif command -v dnf >/dev/null 2>&1; then
  sudo dnf install -y python3 python3-pip gcc-c++ curl
fi
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python app/init_db.py
echo "Install complete. Run: ./run.sh"
