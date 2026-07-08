#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
echo "==================================================="
echo "IndoMarket Insight - One Click Start"
echo "==================================================="
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app/init_db.py
python -m streamlit run app/main.py --server.port 8501
