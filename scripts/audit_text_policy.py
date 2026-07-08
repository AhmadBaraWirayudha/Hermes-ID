"""Audit text policy: no emoji and no literal em dash in text-readable files."""
from pathlib import Path
import re
import sys
ROOT = Path(__file__).resolve().parents[1]
SKIP = {".venv", "__pycache__", ".pytest_cache", ".git", "dist", "build"}
EMOJI_RE = re.compile('[\U0001F300-\U0001FAFF\U00002700-\U000027BF\U00002600-\U000026FF]')

def main():
    bad = []
    for p in ROOT.rglob("*"):
        if not p.is_file() or any(part in SKIP for part in p.relative_to(ROOT).parts):
            continue
        try:
            s = p.read_text(encoding="utf-8")
        except Exception:
            continue
        issues = []
        if "\u2014" in s:
            issues.append("em_dash")
        if EMOJI_RE.search(s):
            issues.append("emoji")
        if issues:
            bad.append((p.relative_to(ROOT), issues))
    if bad:
        print("TEXT POLICY FAILED")
        for rel, issues in bad:
            print(rel, ",".join(issues))
        return 1
    print("TEXT POLICY OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
