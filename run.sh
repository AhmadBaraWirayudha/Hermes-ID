#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python app/init_db.py
streamlit run app/main.py
