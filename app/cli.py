import argparse
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from db import init_db, load_observations
from scraper import make_demo_data, scrape_html_table, scrape_csv_url, scrape_json_api
from exporter import export_dataset
from source_registry import list_sources, get_source
from google_trends import fetch_google_trends, PYTRENDS_TIMEFRAMES
from scraping_ext import scrape_html_selectors, scrape_rss_feed, scrape_sitemap_urls
from reporting import generate_pdf_report, generate_tex_report
from batch_runner import run_active_sources
from source_importer import import_sources_json, export_sources_json
from backtesting import walk_forward_backtest, summarize_backtest
from config import DATA_PROCESSED
from utils import now_stamp
from alerts import evaluate_alerts, save_alerts
from backup import backup_sqlite, backup_workspace, restore_sqlite
from catalog import file_catalog, database_catalog
from notifications import send_webhook, send_email
from exporter import export_parquet
from sentiment import export_sentiment
from model_registry import list_models, export_registry
from scheduler_helper import write_scheduler_snippets, cron_line
from data_studio import growth_metrics


def main():
    parser = argparse.ArgumentParser(description="IndoMarket Insight CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init-db")
    sub.add_parser("demo")
    sub.add_parser("export")
    report = sub.add_parser("report")
    report.add_argument("--format", choices=["pdf", "tex", "both"], default="both")
    sub.add_parser("list-sources")
    sub.add_parser("alerts")
    sub.add_parser("backup-db")
    sub.add_parser("backup-workspace")
    restore = sub.add_parser("restore-db"); restore.add_argument("path")
    sub.add_parser("catalog")
    sub.add_parser("export-parquet")
    sub.add_parser("notify-alerts")
    sub.add_parser("sentiment")
    sub.add_parser("models")
    sub.add_parser("scheduler-snippets")
    sub.add_parser("growth-metrics")
    batch = sub.add_parser("run-active-sources")
    batch.add_argument("--category", default="market")
    batch.add_argument("--region", default="Indonesia")
    batch.add_argument("--limit", type=int, default=None)
    imp = sub.add_parser("import-sources")
    imp.add_argument("path")
    exp = sub.add_parser("export-sources")
    exp.add_argument("path")
    bt = sub.add_parser("backtest")
    bt.add_argument("item")
    bt.add_argument("--horizon", type=int, default=7)
    bt.add_argument("--min-train", type=int, default=45)
    bt.add_argument("--step", type=int, default=7)
    gt = sub.add_parser("google-trends")
    gt.add_argument("keywords", help="Comma-separated keywords, max 5")
    gt.add_argument("--geo", default="ID")
    gt.add_argument("--timeframe", default="today 5-y")
    gt.add_argument("--category", type=int, default=0)
    run = sub.add_parser("run-source")
    run.add_argument("source_id", type=int)
    run.add_argument("--category", default="market")
    run.add_argument("--region", default="Indonesia")
    run.add_argument("--delay", type=float, default=1.0)
    run.add_argument("--no-robots", action="store_true")
    args = parser.parse_args()

    if args.cmd == "init-db":
        init_db(); print("Database initialized")
    elif args.cmd == "demo":
        df = make_demo_data(); print(f"Demo rows generated: {len(df)}")
    elif args.cmd == "export":
        df = load_observations(); csv_path, xlsx_path = export_dataset(df, "cli_export"); print(csv_path); print(xlsx_path)
    elif args.cmd == "report":
        df = load_observations()
        if args.format in ["pdf", "both"]:
            print(generate_pdf_report(df, "IndoMarket Insight CLI Report", "cli_report"))
        if args.format in ["tex", "both"]:
            print(generate_tex_report(df, "IndoMarket Insight CLI Report", "cli_report"))
    elif args.cmd == "list-sources":
        print(list_sources().to_string(index=False))
    elif args.cmd == "alerts":
        alerts_df = evaluate_alerts(load_observations())
        print(alerts_df.to_string(index=False))
        print(save_alerts(alerts_df))
    elif args.cmd == "backup-db":
        print(backup_sqlite())
    elif args.cmd == "backup-workspace":
        print(backup_workspace(include_raw=True))
    elif args.cmd == "restore-db":
        print(restore_sqlite(args.path))
    elif args.cmd == "catalog":
        print("DATABASE")
        print(database_catalog().to_string(index=False))
        print("FILES")
        print(file_catalog().head(100).to_string(index=False))
    elif args.cmd == "export-parquet":
        print(export_parquet(load_observations(), "cli_export"))
    elif args.cmd == "notify-alerts":
        alerts_df = evaluate_alerts(load_observations())
        try:
            print("webhook", send_webhook(alerts_df))
        except Exception as e:
            print("webhook skipped/failed", e)
        try:
            print("email", send_email(alerts_df))
        except Exception as e:
            print("email skipped/failed", e)
    elif args.cmd == "sentiment":
        out, path = export_sentiment(load_observations(), "cli_sentiment")
        print(path)
        print(out[["item", "sentiment_label", "sentiment_score"]].head(20).to_string(index=False))
    elif args.cmd == "models":
        print(list_models().to_string(index=False))
    elif args.cmd == "scheduler-snippets":
        print(write_scheduler_snippets())
        print(cron_line())
    elif args.cmd == "growth-metrics":
        gm = growth_metrics(load_observations())
        out = DATA_PROCESSED / f"{now_stamp()}_cli_growth_metrics.csv"
        gm.to_csv(out, index=False)
        print(out)
    elif args.cmd == "run-active-sources":
        print(run_active_sources(args.category, args.region, limit=args.limit))
    elif args.cmd == "import-sources":
        print(f"Imported {import_sources_json(args.path)} sources")
    elif args.cmd == "export-sources":
        print(export_sources_json(args.path))
    elif args.cmd == "backtest":
        df = load_observations()
        bt = walk_forward_backtest(df, args.item, horizon=args.horizon, min_train=args.min_train, step=args.step)
        out = DATA_PROCESSED / f"{now_stamp()}_{args.item.replace(' ', '_')}_cli_backtest.csv"
        bt.to_csv(out, index=False)
        print(summarize_backtest(bt))
        print(out)
    elif args.cmd == "google-trends":
        clean, raw, processed = fetch_google_trends(args.keywords, geo=args.geo, timeframe=args.timeframe, category=args.category)
        print(f"Rows: {len(clean)}")
        print(processed)
    elif args.cmd == "run-source":
        src = get_source(args.source_id)
        if not src:
            raise SystemExit(f"Source id not found: {args.source_id}")
        if src["source_type"] == "html_table":
            clean, raw, processed = scrape_html_table(src["name"], src["url"], src["table_index"], args.category, args.region, args.delay, not args.no_robots)
        elif src["source_type"] == "csv_url":
            clean, raw, processed = scrape_csv_url(src["name"], src["url"], args.category, args.region, args.delay, not args.no_robots)
        elif src["source_type"] == "json_api":
            clean, raw, processed = scrape_json_api(src["name"], src["url"], None, args.category, args.region, args.delay, not args.no_robots)
        elif src["source_type"] == "html_selectors":
            clean, raw, processed = scrape_html_selectors(src["name"], src["url"], src.get("notes") or "{}", args.category, args.region, args.delay, not args.no_robots)
        elif src["source_type"] == "rss_feed":
            clean, raw, processed = scrape_rss_feed(src["name"], src["url"], args.category, args.region, args.delay, not args.no_robots)
        else:
            clean, raw, processed = scrape_sitemap_urls(src["name"], src["url"], src.get("notes") or "", 200, args.delay, not args.no_robots)
        print(f"Rows: {len(clean)}")
        print(f"Raw: {raw}")
        print(f"Processed: {processed}")

if __name__ == "__main__":
    main()
