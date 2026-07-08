"""Batch runner for all active configured sources."""
from source_registry import list_sources
from scraper import scrape_html_table, scrape_csv_url, scrape_json_api
from scraping_ext import scrape_html_selectors, scrape_rss_feed, scrape_sitemap_urls


def run_active_sources(category="market", region="Indonesia", delay=1.0, respect_robots=True, limit=None):
    sources = list_sources(active_only=True)
    results = []
    if limit:
        sources = sources.head(int(limit))
    for _, src in sources.iterrows():
        try:
            if src["source_type"] == "html_table":
                clean, raw, processed = scrape_html_table(src["name"], src["url"], src["table_index"], category, region, delay, respect_robots)
            elif src["source_type"] == "csv_url":
                clean, raw, processed = scrape_csv_url(src["name"], src["url"], category, region, delay, respect_robots)
            elif src["source_type"] == "json_api":
                clean, raw, processed = scrape_json_api(src["name"], src["url"], None, category, region, delay, respect_robots)
            elif src["source_type"] == "html_selectors":
                clean, raw, processed = scrape_html_selectors(src["name"], src["url"], src.get("notes") or "{}", category, region, delay, respect_robots)
            elif src["source_type"] == "rss_feed":
                clean, raw, processed = scrape_rss_feed(src["name"], src["url"], category, region, delay, respect_robots)
            else:
                clean, raw, processed = scrape_sitemap_urls(src["name"], src["url"], src.get("notes") or "", 200, delay, respect_robots)
            results.append({"source": src["name"], "status": "success", "rows": len(clean), "processed": str(processed)})
        except Exception as e:
            results.append({"source": src.get("name", "unknown"), "status": "failed", "rows": 0, "error": str(e)})
    return results
