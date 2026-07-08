import sys
import urllib.request

urls = sys.argv[1:] or ["http://localhost:8000/health", "http://localhost:8501/_stcore/health"]
failed = []
for url in urls:
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            print(url, r.status)
            if r.status >= 500:
                failed.append(url)
    except Exception as e:
        print(url, "FAILED", e)
        failed.append(url)
if failed:
    raise SystemExit(1)
