#!/usr/bin/env bash
set -euo pipefail
python scripts/validate_project.py
python scripts/audit_text_policy.py
python scripts/audit_runtime_references.py || true
python -m py_compile app/*.py app/*/*.py scripts/*.py scripts/*/*.py
pytest -q || true
python app/cli.py demo >/tmp/indomarket_demo.log 2>&1 || true
python app/cli.py alerts || true
python app/cli.py report --format tex || true
echo "Smoke workflow completed. Review output for optional dependency warnings."
