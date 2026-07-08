"""Light audit for user-facing text that should stay friendly."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
TARGETS = [ROOT / "app" / "main.py", ROOT / "START_HERE_ONE_CLICK.md", ROOT / "QUICK_START_5_SECONDS.md", ROOT / "docs" / "simple"]
HARD_WORDS = [
    "utilize", "aforementioned", "henceforth", "notwithstanding", "therein", "heretofore",
    "subsequently", "commence", "terminate", "leverage synergies"
]

def files():
    for t in TARGETS:
        if t.is_file():
            yield t
        elif t.is_dir():
            yield from t.rglob("*.md")

def main():
    hits = []
    for p in files():
        text = p.read_text(encoding="utf-8", errors="ignore").lower()
        for word in HARD_WORDS:
            if word in text:
                hits.append((p.relative_to(ROOT), word))
    if hits:
        print("FRIENDLY LANGUAGE CHECK FAILED")
        for rel, word in hits:
            print(rel, word)
        return 1
    print("FRIENDLY LANGUAGE CHECK OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
