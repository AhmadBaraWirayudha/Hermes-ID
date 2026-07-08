"""One-command automated pipeline for scheduled/cron use."""
import argparse
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from db import init_db, load_observations
from batch_runner import run_active_sources
from scraper import make_demo_data
from exporter import export_dataset
from reporting import generate_pdf_report, generate_tex_report
from alerts import evaluate_alerts, save_alerts


def main():
    parser = argparse.ArgumentParser(description="Run IndoMarket automated pipeline")
    parser.add_argument("--demo-if-empty", action="store_true")
    parser.add_argument("--run-sources", action="store_true")
    parser.add_argument("--category", default="market")
    parser.add_argument("--region", default="Indonesia")
    parser.add_argument("--export", action="store_true")
    parser.add_argument("--report", choices=["none", "pdf", "tex", "both"], default="none")
    parser.add_argument("--alerts", action="store_true")
    args = parser.parse_args()

    init_db()
    if args.run_sources:
        print("Sources:", run_active_sources(args.category, args.region))
    df = load_observations()
    if args.demo_if_empty and df.empty:
        make_demo_data(); df = load_observations()
    if args.alerts:
        alerts = evaluate_alerts(df); print(alerts.to_string(index=False)); print(save_alerts(alerts))
    if args.export:
        print(export_dataset(df, "pipeline_export"))
    if args.report in ["pdf", "both"]:
        print(generate_pdf_report(df, "IndoMarket Insight Pipeline Report", "pipeline_report"))
    if args.report in ["tex", "both"]:
        print(generate_tex_report(df, "IndoMarket Insight Pipeline Report", "pipeline_report"))

if __name__ == "__main__":
    main()
