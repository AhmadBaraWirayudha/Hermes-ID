#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
g++ -O3 -fPIC -shared market_math.cpp -o libmarket_math.so
echo "Built cpp/libmarket_math.so"
