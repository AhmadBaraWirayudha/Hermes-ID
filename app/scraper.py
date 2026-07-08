import json
import time
import urllib.robotparser
from urllib.parse import urlparse
from pathlib import Path
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
try:
    from apscheduler.schedulers.background import BackgroundScheduler
except Exception:
    BackgroundScheduler = None
from config import DATA_RAW, DATA_PROCESSED
from utils import now_stamp, normalize_market_df
from db import upsert_observations, log_scrape

HEADERS = {
    "User-Agent": "IndoMarketInsight/0.2 (+respectful research scraper; contact: local-user)"
}


def is_allowed_by_robots(url: str, user_agent: str = HEADERS["User-Agent"]):
    """Best-effort robots.txt check. If robots cannot be fetched, warn but do not hard fail."""
    try:
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception:
        return True


def scrape_html_table(name: str, url: str, table_index: int = 0, category="market", region="Indonesia", delay_seconds=1.0, respect_robots=True):
    stamp = now_stamp()
    raw_path = DATA_RAW / f"{stamp}_{name}_raw.csv"
    processed_path = DATA_PROCESSED / f"{stamp}_{name}_processed.csv"
    try:
        if respect_robots and not is_allowed_by_robots(url):
            raise PermissionError("robots.txt appears to disallow scraping this URL")
        time.sleep(float(delay_seconds or 0))
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        tables = pd.read_html(response.text, flavor="lxml")
        raw = tables[int(table_index)]
        raw.to_csv(raw_path, index=False)
        clean = normalize_market_df(raw, source=name, default_category=category, default_region=region)
        clean.to_csv(processed_path, index=False)
        rows = upsert_observations(clean)
        log_scrape(name, "success", rows, raw_path, processed_path, "html table scrape")
        return clean, raw_path, processed_path
    except Exception as e:
        log_scrape(name, "failed", 0, raw_path, None, str(e))
        raise


def scrape_csv_url(name: str, url: str, category="market", region="Indonesia", delay_seconds=1.0, respect_robots=True):
    stamp = now_stamp()
    raw_path = DATA_RAW / f"{stamp}_{name}_raw.csv"
    processed_path = DATA_PROCESSED / f"{stamp}_{name}_processed.csv"
    try:
        if respect_robots and not is_allowed_by_robots(url):
            raise PermissionError("robots.txt appears to disallow scraping this URL")
        time.sleep(float(delay_seconds or 0))
        raw = pd.read_csv(url)
        raw.to_csv(raw_path, index=False)
        clean = normalize_market_df(raw, source=name, default_category=category, default_region=region)
        clean.to_csv(processed_path, index=False)
        rows = upsert_observations(clean)
        log_scrape(name, "success", rows, raw_path, processed_path, "csv url scrape")
        return clean, raw_path, processed_path
    except Exception as e:
        log_scrape(name, "failed", 0, raw_path, None, str(e))
        raise


def scrape_json_api(name: str, url: str, record_path=None, category="market", region="Indonesia", delay_seconds=1.0, respect_robots=True):
    stamp = now_stamp()
    raw_path = DATA_RAW / f"{stamp}_{name}_raw.json"
    processed_path = DATA_PROCESSED / f"{stamp}_{name}_processed.csv"
    try:
        if respect_robots and not is_allowed_by_robots(url):
            raise PermissionError("robots.txt appears to disallow scraping this URL")
        time.sleep(float(delay_seconds or 0))
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        data = r.json()
        raw_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        raw = pd.json_normalize(data if record_path is None else data[record_path])
        clean = normalize_market_df(raw, source=name, default_category=category, default_region=region)
        clean.to_csv(processed_path, index=False)
        rows = upsert_observations(clean)
        log_scrape(name, "success", rows, raw_path, processed_path, "json api scrape")
        return clean, raw_path, processed_path
    except Exception as e:
        log_scrape(name, "failed", 0, raw_path, None, str(e))
        raise


def import_csv(file, name="manual_csv", category="market", region="Indonesia"):
    stamp = now_stamp()
    raw_path = DATA_RAW / f"{stamp}_{name}_upload.csv"
    processed_path = DATA_PROCESSED / f"{stamp}_{name}_processed.csv"
    raw = pd.read_csv(file)
    raw.to_csv(raw_path, index=False)
    clean = normalize_market_df(raw, source=name, default_category=category, default_region=region)
    clean.to_csv(processed_path, index=False)
    rows = upsert_observations(clean)
    log_scrape(name, "success", rows, raw_path, processed_path, "manual csv import")
    return clean, raw_path, processed_path


def make_demo_data():
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=120)
    rows = []
    items = ["Beras Premium", "Minyak Goreng", "Gula Pasir", "BBCA.JK", "TLKM.JK"]
    base = [15500, 18000, 16500, 9600, 3100]
    for item, b in zip(items, base):
        for i, d in enumerate(dates):
            seasonal = 1 + 0.03 * np.sin(i / 9)
            noise = ((hash((item, str(d.date()))) % 100) - 50) / 1000
            price = b * (1 + i * 0.0009 + noise) * seasonal
            rows.append({"date": d.date().isoformat(), "source": "demo", "category": "commodity" if ".JK" not in item else "idx_stock", "item": item, "region": "Indonesia", "price": round(price, 2), "volume": None, "metric": "price", "currency": "IDR", "raw_payload": None})
    df = pd.DataFrame(rows)
    processed_path = DATA_PROCESSED / f"{now_stamp()}_demo_processed.csv"
    df.to_csv(processed_path, index=False)
    rows_count = upsert_observations(df)
    log_scrape("demo", "success", rows_count, None, processed_path, "generated demo Indonesian market data")
    return df


class AutoScrapeScheduler:
    def __init__(self):
        if BackgroundScheduler is None:
            raise RuntimeError("APScheduler is not installed. Run: pip install -r requirements.txt")
        self.scheduler = BackgroundScheduler(timezone="Asia/Jakarta")

    def start_html_table_job(self, name, url, minutes=60, table_index=0, category="market", region="Indonesia"):
        if not self.scheduler.running:
            self.scheduler.start()
        job_id = f"scrape_{name}"
        self.scheduler.add_job(
            scrape_html_table, "interval", minutes=minutes, id=job_id, replace_existing=True,
            args=[name, url, table_index, category, region]
        )
        return job_id
