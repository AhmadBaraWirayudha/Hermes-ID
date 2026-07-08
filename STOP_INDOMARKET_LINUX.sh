#!/usr/bin/env bash
set -euo pipefail
pkill -f "streamlit run app/main.py" || true
pkill -f "uvicorn app.api:api" || true
echo "Stopped matching IndoMarket Insight processes."
