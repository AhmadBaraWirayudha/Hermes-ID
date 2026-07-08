"""Expanded scraping connectors beyond basic tables/CSV/JSON."""
import json
import time
import xml.etree.ElementTree as ET
from urllib.parse import urljoin
import pandas as pd
import requests
from bs4 import BeautifulSoup
from config import DATA_RAW, DATA_PROCESSED
from utils import now_stamp, normalize_market_df
from db import upsert_observations, log_scrape
from scraper import HEADERS, is_allowed_by_robots


def scrape_html_selectors(name, url, selectors, category="web", region="Indonesia", delay_seconds=1.0, respect_robots=True):
    """Scrape repeated HTML elements using CSS selectors.

    selectors example: {"container":".product", "item":".name", "price":".price", "date":".date"}
    If container omitted, selectors are evaluated document-wide.
    """
    if isinstance(selectors, str):
        selectors = json.loads(selectors)
    if respect_robots and not is_allowed_by_robots(url):
        raise PermissionError("robots.txt appears to disallow scraping this URL")
    time.sleep(float(delay_seconds or 0))
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    containers = soup.select(selectors.get("container")) if selectors.get("container") else [soup]
    rows = []
    fields = [k for k in selectors.keys() if k != "container"]
    for c in containers:
        row = {}
        for field in fields:
            el = c.select_one(selectors[field])
            row[field] = el.get_text(" ", strip=True) if el else None
        if any(v for v in row.values()):
            rows.append(row)
    raw = pd.DataFrame(rows)
    stamp = now_stamp()
    raw_path = DATA_RAW / f"{stamp}_{name}_selectors_raw.csv"
    processed_path = DATA_PROCESSED / f"{stamp}_{name}_selectors_processed.csv"
    raw.to_csv(raw_path, index=False)
    clean = normalize_market_df(raw, source=name, default_category=category, default_region=region)
    clean.to_csv(processed_path, index=False)
    count = upsert_observations(clean)
    log_scrape(name, "success", count, raw_path, processed_path, "html css selector scrape")
    return clean, raw_path, processed_path


def scrape_rss_feed(name, url, category="news", region="Indonesia", delay_seconds=1.0, respect_robots=True):
    if respect_robots and not is_allowed_by_robots(url):
        raise PermissionError("robots.txt appears to disallow scraping this URL")
    time.sleep(float(delay_seconds or 0))
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    root = ET.fromstring(r.content)
    rows = []
    for item in root.findall(".//item"):
        title = item.findtext("title")
        pub = item.findtext("pubDate")
        link = item.findtext("link")
        rows.append({"date": pub, "item": title, "price": 1, "volume": None, "metric": "article_count", "url": link})
    raw = pd.DataFrame(rows)
    stamp = now_stamp()
    raw_path = DATA_RAW / f"{stamp}_{name}_rss_raw.csv"
    processed_path = DATA_PROCESSED / f"{stamp}_{name}_rss_processed.csv"
    raw.to_csv(raw_path, index=False)
    clean = normalize_market_df(raw, source=name, default_category=category, default_region=region)
    clean.to_csv(processed_path, index=False)
    count = upsert_observations(clean)
    log_scrape(name, "success", count, raw_path, processed_path, "rss feed scrape")
    return clean, raw_path, processed_path


def scrape_sitemap_urls(name, sitemap_url, contains="", max_urls=200, delay_seconds=1.0, respect_robots=True):
    if respect_robots and not is_allowed_by_robots(sitemap_url):
        raise PermissionError("robots.txt appears to disallow scraping this sitemap")
    time.sleep(float(delay_seconds or 0))
    r = requests.get(sitemap_url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    root = ET.fromstring(r.content)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = [el.text for el in root.findall(".//sm:loc", ns)] or [el.text for el in root.findall(".//loc")]
    if contains:
        locs = [u for u in locs if contains in u]
    locs = locs[:int(max_urls)]
    raw = pd.DataFrame({"date": pd.Timestamp.today().date().isoformat(), "item": locs, "price": 1, "metric": "url_discovered"})
    stamp = now_stamp()
    raw_path = DATA_RAW / f"{stamp}_{name}_sitemap_raw.csv"
    processed_path = DATA_PROCESSED / f"{stamp}_{name}_sitemap_processed.csv"
    raw.to_csv(raw_path, index=False)
    clean = normalize_market_df(raw, source=name, default_category="sitemap", default_region="Indonesia")
    clean.to_csv(processed_path, index=False)
    count = upsert_observations(clean)
    log_scrape(name, "success", count, raw_path, processed_path, "sitemap url extraction")
    return clean, raw_path, processed_path


def scrape_paginated_tables(name, url_template, start_page=1, end_page=3, table_index=0, category="market", region="Indonesia", delay_seconds=1.0):
    """Scrape tables across pages. url_template must contain {page}."""
    from scraper import scrape_html_table
    frames = []
    raw_paths, processed_paths = [], []
    for page in range(int(start_page), int(end_page) + 1):
        url = url_template.format(page=page)
        clean, raw, processed = scrape_html_table(f"{name}_p{page}", url, table_index, category, region, delay_seconds, True)
        frames.append(clean); raw_paths.append(raw); processed_paths.append(processed)
    all_clean = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    return all_clean, raw_paths, processed_paths
