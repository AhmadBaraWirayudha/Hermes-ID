"""Self-repair workflow for local project setup."""
from __future__ import annotations
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app"


def run(cmd, allow_fail=False):
    print("RUN", " ".join(map(str, cmd)))
    p = subprocess.run(cmd, cwd=ROOT)
    if p.returncode and not allow_fail:
        raise SystemExit(p.returncode)
    return p.returncode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="Generate demo data if database has no observations")
    parser.add_argument("--skip-tests", action="store_true")
    args = parser.parse_args()

    for rel in ["data/raw", "data/processed", "models", "logs", "config", "backups"]:
        (ROOT / rel).mkdir(parents=True, exist_ok=True)

    sys.path.insert(0, str(APP))
    from db import init_db, load_observations
    init_db()
    if args.demo and load_observations().empty:
        from scraper import make_demo_data
        make_demo_data()

    run([sys.executable, "scripts/validate_project.py"])
    run([sys.executable, "scripts/audit_text_policy.py"])
    run([sys.executable, "scripts/audit_runtime_references.py"])
    run([sys.executable, "-m", "py_compile", *[str(p.relative_to(ROOT)) for p in list((ROOT / "app").glob("*.py"))]])
    if not args.skip_tests:
        run([sys.executable, "-m", "pytest", "-q"], allow_fail=True)
    run([sys.executable, "scripts/generate_project_inventory.py"])
    run([sys.executable, "scripts/create_debug_bundle.py"])
    print("Repair workflow complete")


if __name__ == "__main__":
    main()
