"""Generate scheduler snippets for cron/Windows Task Scheduler."""
from pathlib import Path
from config import ROOT, DATA_PROCESSED
from utils import now_stamp


def cron_line(project_path=None, hour=7, minute=0, command_args="--demo-if-empty --alerts --export --report both"):
    project_path = Path(project_path or ROOT).resolve()
    return f"{int(minute)} {int(hour)} * * * cd {project_path} && . .venv/bin/activate && python app/pipeline.py {command_args} >> logs/pipeline.log 2>&1"


def systemd_timer_files(service_name="indomarket-pipeline", hour=7, minute=0):
    service = f"""[Unit]\nDescription=IndoMarket Insight Pipeline\n\n[Service]\nType=oneshot\nWorkingDirectory={ROOT}\nExecStart={ROOT}/.venv/bin/python app/pipeline.py --demo-if-empty --alerts --export --report both\n"""
    timer = f"""[Unit]\nDescription=Run IndoMarket Insight Pipeline daily\n\n[Timer]\nOnCalendar=*-*-* {int(hour):02d}:{int(minute):02d}:00\nPersistent=true\n\n[Install]\nWantedBy=timers.target\n"""
    return service, timer


def write_scheduler_snippets(hour=7, minute=0):
    stamp = now_stamp()
    cron_path = DATA_PROCESSED / f"{stamp}_cron_snippet.txt"
    service_path = DATA_PROCESSED / f"{stamp}_indomarket-pipeline.service"
    timer_path = DATA_PROCESSED / f"{stamp}_indomarket-pipeline.timer"
    cron_path.write_text(cron_line(hour=hour, minute=minute), encoding="utf-8")
    service, timer = systemd_timer_files(hour=hour, minute=minute)
    service_path.write_text(service, encoding="utf-8")
    timer_path.write_text(timer, encoding="utf-8")
    return cron_path, service_path, timer_path
