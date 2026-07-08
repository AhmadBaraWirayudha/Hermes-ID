"""Real-time OSINT monitoring for geopolitical, market, news, and social signals.

Compliance notes:
- Prefer official APIs and RSS feeds.
- Respect robots.txt and site terms.
- Do not bypass authentication, paywalls, rate limits, CAPTCHAs, or technical controls.
- Social media collection should use official APIs, approved exports, or user-provided CSV files.
"""
from __future__ import annotations
import json
import re
import sqlite3
import time
import urllib.robotparser
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

from config import DB_PATH, DATA_RAW, DATA_PROCESSED, ROOT
from sentiment import score_text
from utils import now_stamp

HEADERS = {
    "User-Agent": "HermesAnalyticsID-OSINT/0.1 respectful monitor"
}

OSINT_SCHEMA = """
CREATE TABLE IF NOT EXISTS osint_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    url TEXT NOT NULL,
    source_type TEXT NOT NULL DEFAULT 'rss',
    category TEXT DEFAULT 'news',
    country TEXT DEFAULT 'ID',
    active INTEGER NOT NULL DEFAULT 1,
    crawl_depth INTEGER DEFAULT 0,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS osint_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    observed_at TEXT NOT NULL,
    published_at TEXT,
    source TEXT NOT NULL,
    source_type TEXT NOT NULL,
    category TEXT DEFAULT 'news',
    country TEXT DEFAULT 'ID',
    title TEXT,
    url TEXT,
    content TEXT,
    keywords TEXT,
    sentiment_score REAL,
    sentiment_label TEXT,
    raw_payload TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source, url, title)
);

CREATE TABLE IF NOT EXISTS osint_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    finished_at TEXT,
    status TEXT NOT NULL,
    source TEXT,
    rows_collected INTEGER DEFAULT 0,
    message TEXT
);

CREATE TABLE IF NOT EXISTS tension_indicators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    observed_at TEXT NOT NULL,
    indicator_name TEXT NOT NULL,
    source TEXT NOT NULL,
    url TEXT,
    level TEXT,
    score REAL,
    summary TEXT,
    raw_text TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(observed_at, indicator_name, source)
);
"""

DEFAULT_KEYWORDS = [
    "indonesia", "bank indonesia", "bi rate", "idx", "ihsg", "rupiah", "idr",
    "nickel", "coal", "cpo", "palm oil", "minyak sawit", "geopolitik",
    "militer", "tension", "defcon", "election", "inflation", "inflasi",
    "sbn", "reksa dana", "ojk", "bappebti", "komoditas"
]

PENTAGON_PIZZA_URL = "https://www.defconlevel.com/"


@dataclass
class OsintSource:
    name: str
    url: str
    source_type: str = "rss"
    category: str = "news"
    country: str = "ID"
    active: bool = True
    crawl_depth: int = 0
    notes: str = ""


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_osint_db():
    with connect() as conn:
        conn.executescript(OSINT_SCHEMA)


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def is_allowed_by_robots(url: str, user_agent: str = HEADERS["User-Agent"]):
    try:
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception:
        return True


def add_osint_source(src: OsintSource):
    init_osint_db()
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO osint_sources(name, url, source_type, category, country, active, crawl_depth, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                url=excluded.url,
                source_type=excluded.source_type,
                category=excluded.category,
                country=excluded.country,
                active=excluded.active,
                crawl_depth=excluded.crawl_depth,
                notes=excluded.notes
            """,
            (src.name, src.url, src.source_type, src.category, src.country, 1 if src.active else 0, src.crawl_depth, src.notes),
        )


def import_osint_sources_json(path_or_file):
    if hasattr(path_or_file, "read"):
        raw = path_or_file.read()
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")
        data = json.loads(raw)
    else:
        data = json.loads(Path(path_or_file).read_text(encoding="utf-8"))
    count = 0
    for row in data:
        add_osint_source(OsintSource(**row))
        count += 1
    return count


def list_osint_sources(active_only=False):
    init_osint_db()
    where = "WHERE active = 1" if active_only else ""
    with connect() as conn:
        return pd.read_sql_query(f"SELECT * FROM osint_sources {where} ORDER BY name", conn)


def insert_events(events):
    if not events:
        return 0
    init_osint_db()
    rows = []
    for e in events:
        sent = score_text((e.get("title") or "") + " " + (e.get("content") or ""))
        rows.append((
            e.get("observed_at") or utc_now(),
            e.get("published_at"),
            e.get("source"),
            e.get("source_type"),
            e.get("category", "news"),
            e.get("country", "ID"),
            e.get("title"),
            e.get("url"),
            e.get("content"),
            json.dumps(e.get("keywords", []), ensure_ascii=False),
            sent["sentiment_score"],
            sent["sentiment_label"],
            json.dumps(e.get("raw_payload", {}), ensure_ascii=False),
        ))
    with connect() as conn:
        conn.executemany(
            """
            INSERT INTO osint_events
            (observed_at, published_at, source, source_type, category, country, title, url, content, keywords, sentiment_score, sentiment_label, raw_payload)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(source, url, title) DO UPDATE SET
                observed_at=excluded.observed_at,
                content=excluded.content,
                keywords=excluded.keywords,
                sentiment_score=excluded.sentiment_score,
                sentiment_label=excluded.sentiment_label,
                raw_payload=excluded.raw_payload
            """,
            rows,
        )
    return len(rows)


def log_run(source, status, rows=0, message=""):
    init_osint_db()
    with connect() as conn:
        conn.execute(
            "INSERT INTO osint_runs(source, status, rows_collected, message, finished_at) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)",
            (source, status, rows, message),
        )


def keyword_hits(text, keywords=None):
    keywords = keywords or DEFAULT_KEYWORDS
    low = str(text or "").lower()
    return [k for k in keywords if k.lower() in low]


def fetch_rss_source(src: OsintSource, keywords=None, timeout=30):
    try:
        import feedparser
    except Exception as exc:
        raise ImportError("feedparser is required for RSS monitoring. Install requirements.txt") from exc
    if not is_allowed_by_robots(src.url):
        raise PermissionError("robots.txt appears to disallow this RSS URL")
    feed = feedparser.parse(src.url)
    events = []
    for entry in feed.entries[:100]:
        title = getattr(entry, "title", "")
        link = getattr(entry, "link", src.url)
        summary = getattr(entry, "summary", "")
        published = getattr(entry, "published", None) or getattr(entry, "updated", None)
        hits = keyword_hits(f"{title} {summary}", keywords)
        events.append({
            "source": src.name,
            "source_type": "rss",
            "category": src.category,
            "country": src.country,
            "title": title,
            "url": link,
            "content": BeautifulSoup(summary, "html.parser").get_text(" ", strip=True) if summary else "",
            "published_at": published,
            "keywords": hits,
            "raw_payload": dict(entry),
        })
    return events


def parse_html_page(src: OsintSource, keywords=None, timeout=30):
    if not is_allowed_by_robots(src.url):
        raise PermissionError("robots.txt appears to disallow this URL")
    r = requests.get(src.url, headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else src.url
    meta = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
    desc = meta.get("content", "") if meta else ""
    text = " ".join([title, desc])
    events = [{
        "source": src.name,
        "source_type": src.source_type,
        "category": src.category,
        "country": src.country,
        "title": title,
        "url": src.url,
        "content": desc,
        "keywords": keyword_hits(text, keywords),
        "raw_payload": {"title": title, "description": desc},
    }]
    if src.crawl_depth > 0:
        base = f"{urlparse(src.url).scheme}://{urlparse(src.url).netloc}"
        links = []
        for a in soup.select("a[href]")[:80]:
            href = urljoin(base, a.get("href"))
            if urlparse(href).netloc == urlparse(src.url).netloc:
                links.append(href)
        for link in sorted(set(links))[:20]:
            try:
                child = OsintSource(src.name, link, src.source_type, src.category, src.country, True, 0, src.notes)
                events.extend(parse_html_page(child, keywords, timeout=timeout))
                time.sleep(0.2)
            except Exception:
                continue
    return events


def import_social_csv(file_or_path, source_name="social_media_import", platform="social", country="ID"):
    init_osint_db()
    df = pd.read_csv(file_or_path)
    events = []
    for _, row in df.iterrows():
        text = str(row.get("text", row.get("content", row.get("title", ""))))
        events.append({
            "source": source_name,
            "source_type": platform,
            "category": "social_media",
            "country": country,
            "title": text[:180],
            "url": row.get("url"),
            "content": text,
            "published_at": row.get("published_at", row.get("date")),
            "keywords": keyword_hits(text),
            "raw_payload": row.to_dict(),
        })
    return insert_events(events)


def monitor_source(row, keywords=None):
    src = OsintSource(
        name=row["name"], url=row["url"], source_type=row.get("source_type", "rss"),
        category=row.get("category", "news"), country=row.get("country", "ID"),
        active=bool(row.get("active", 1)), crawl_depth=int(row.get("crawl_depth", 0) or 0), notes=row.get("notes") or ""
    )
    if src.source_type == "rss":
        events = fetch_rss_source(src, keywords)
    elif src.source_type in ["web", "html", "crawler"]:
        events = parse_html_page(src, keywords)
    else:
        raise ValueError(f"Unsupported source type for automatic monitoring: {src.source_type}")
    rows = insert_events(events)
    log_run(src.name, "success", rows, "monitor source")
    return rows


def run_osint_cycle(keywords=None, active_only=True, limit=None):
    init_osint_db()
    sources = list_osint_sources(active_only=active_only)
    if limit:
        sources = sources.head(int(limit))
    results = []
    for _, row in sources.iterrows():
        try:
            rows = monitor_source(row, keywords)
            results.append({"source": row["name"], "status": "success", "rows": rows})
        except Exception as e:
            log_run(row.get("name", "unknown"), "failed", 0, str(e))
            results.append({"source": row.get("name", "unknown"), "status": "failed", "rows": 0, "message": str(e)})
    return pd.DataFrame(results)


def load_osint_events(limit=500, category=None, keyword=None):
    init_osint_db()
    sql = "SELECT * FROM osint_events"
    params = []
    where = []
    if category:
        where.append("category = ?")
        params.append(category)
    if keyword:
        where.append("LOWER(title || ' ' || content || ' ' || keywords) LIKE ?")
        params.append(f"%{keyword.lower()}%")
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY observed_at DESC LIMIT ?"
    params.append(int(limit))
    with connect() as conn:
        return pd.read_sql_query(sql, conn, params=params)


def load_osint_runs(limit=200):
    init_osint_db()
    with connect() as conn:
        return pd.read_sql_query("SELECT * FROM osint_runs ORDER BY started_at DESC LIMIT ?", conn, params=(int(limit),))


def monitor_pentagon_pizza_index(url=PENTAGON_PIZZA_URL):
    init_osint_db()
    if not is_allowed_by_robots(url):
        raise PermissionError("robots.txt appears to disallow this URL")
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text(" ", strip=True)
    low = text.lower()
    snippets = []
    for term in ["pentagon pizza", "pizza index", "defcon", "threat", "tension"]:
        idx = low.find(term)
        if idx >= 0:
            snippets.append(text[max(0, idx - 180): idx + 360])
    summary = " | ".join(snippets[:3]) or text[:800]
    level_match = re.search(r"DEFCON\s*(?:Level)?\s*[:#-]?\s*([0-9]+)", text, re.IGNORECASE)
    score_match = re.search(r"Pizza\s*Index\s*[:#-]?\s*([0-9]+(?:\.[0-9]+)?)", text, re.IGNORECASE)
    level = level_match.group(1) if level_match else None
    score = float(score_match.group(1)) if score_match else None
    observed = utc_now()
    with connect() as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO tension_indicators
            (observed_at, indicator_name, source, url, level, score, summary, raw_text)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (observed, "Pentagon Pizza Index", "defconlevel.com", url, level, score, summary, text[:5000]),
        )
    processed = DATA_PROCESSED / f"{now_stamp()}_pentagon_pizza_index.json"
    processed.write_text(json.dumps({"observed_at": observed, "level": level, "score": score, "summary": summary, "url": url}, indent=2), encoding="utf-8")
    log_run("Pentagon Pizza Index", "success", 1, "tension indicator monitor")
    return {"observed_at": observed, "level": level, "score": score, "summary": summary, "url": url}


def load_tension_indicators(limit=100):
    init_osint_db()
    with connect() as conn:
        return pd.read_sql_query("SELECT * FROM tension_indicators ORDER BY observed_at DESC LIMIT ?", conn, params=(int(limit),))


def seed_default_osint_sources():
    init_osint_db()
    default_path = ROOT / "config" / "osint_sources.example.json"
    if default_path.exists():
        return import_osint_sources_json(default_path)
    return 0
