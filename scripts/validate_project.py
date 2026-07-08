"""Validate project structure and required files."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "requirements.txt",
    "app/main.py",
    "app/api.py",
    "app/cli.py",
    "sql/schema.sql",
    "docs/architecture/production_layers.md",
    "podman-compose.prod.yml",
    "Containerfile",
]
SKIP_DIRS = {".venv", "__pycache__", ".pytest_cache", "node_modules", "dist", "build"}

def main():
    errors = []
    for rel in REQUIRED:
        if not (ROOT / rel).exists():
            errors.append(f"Missing required file: {rel}")
    for d in [ROOT] + [p for p in ROOT.rglob("*") if p.is_dir()]:
        if any(part in SKIP_DIRS for part in d.relative_to(ROOT).parts):
            continue
        if not (d / "README.md").exists():
            errors.append(f"Folder missing README.md: {d.relative_to(ROOT)}")
    if errors:
        print("PROJECT VALIDATION FAILED")
        for e in errors:
            print(" -", e)
        return 1
    print("PROJECT VALIDATION OK")
    print(f"Root: {ROOT}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
