#!/usr/bin/env bash
set -euo pipefail
if [[ ! -d .venv ]]; then python3 -m venv .venv; fi
. .venv/bin/activate
pip install --no-index --find-links wheelhouse -r requirements.txt
python app/init_db.py
echo "Installed from local wheelhouse."
