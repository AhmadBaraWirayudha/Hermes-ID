"""Background task scaffolding.

For small deployments, call functions directly. For production, wire these functions
to Celery/RQ/Arq/Cloud Tasks. They are deliberately plain Python to avoid lock-in.
"""
from db import load_observations
from batch_runner import run_active_sources
from alerts import evaluate_alerts, save_alerts
from exporter import export_dataset
from reporting import generate_pdf_report, generate_tex_report
from model_registry import list_models


def task_run_sources(category="market", region="Indonesia", limit=None):
    return run_active_sources(category=category, region=region, limit=limit)


def task_alerts():
    alerts = evaluate_alerts(load_observations())
    path = save_alerts(alerts)
    return {"rows": len(alerts), "path": str(path)}


def task_export_all():
    csv_path, xlsx_path = export_dataset(load_observations(), "worker_export")
    return {"csv": str(csv_path), "xlsx": str(xlsx_path)}


def task_report_all():
    df = load_observations()
    pdf = generate_pdf_report(df, "IndoMarket Insight Worker Report", "worker_report")
    tex = generate_tex_report(df, "IndoMarket Insight Worker Report", "worker_report")
    return {"pdf": str(pdf), "tex": str(tex)}


def task_model_inventory():
    return list_models().to_dict(orient="records")
