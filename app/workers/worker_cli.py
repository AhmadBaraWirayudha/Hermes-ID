import argparse
from tasks import task_run_sources, task_alerts, task_export_all, task_report_all, task_model_inventory

TASKS = {
    "run-sources": task_run_sources,
    "alerts": task_alerts,
    "export": task_export_all,
    "report": task_report_all,
    "models": task_model_inventory,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IndoMarket worker task runner")
    parser.add_argument("task", choices=TASKS.keys())
    args = parser.parse_args()
    print(TASKS[args.task]())
