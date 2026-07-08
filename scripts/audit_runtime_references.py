"""Audit runtime references for old container commands.

Allowed: migration docs that explain old-to-new mapping and OCI image source names.
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
ALLOW = {
    "docs/deployment/container_runtime_migration.md",
    "docs/deployment/podman_windows_cloud.md",
    "Containerfile",
    "podman-compose.yml",
    "podman-compose.prod.yml",
    "podman-compose.storage.yml",
    "scripts/audit_runtime_references.py",
}
NEEDLES = ["docker compose", "docker-compose.yml", "docker-compose.prod.yml", "Dockerfile"]

def main():
    hits = []
    for p in ROOT.rglob("*"):
        if not p.is_file() or any(part in {".venv", "__pycache__", ".pytest_cache", ".git"} for part in p.relative_to(ROOT).parts):
            continue
        rel = str(p.relative_to(ROOT))
        if rel in ALLOW:
            continue
        try:
            s = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        low = s.lower()
        for n in NEEDLES:
            if n.lower() in low:
                hits.append((rel, n))
    if hits:
        print("OLD RUNTIME REFERENCES FOUND")
        for h in hits[:100]:
            print(h[0], h[1])
        return 1
    print("RUNTIME REFERENCES OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
