"""Run real-time monitor every five minutes.

Usage:
  python scripts/run_realtime_monitor.py --once
  python scripts/run_realtime_monitor.py --interval 300
"""
from __future__ import annotations
import argparse
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))
from realtime_engine import run_realtime_cycle, realtime_status, seed_watchlist
from osint_monitor import seed_default_osint_sources


def cycle(include_pizza=True):
    seed_default_osint_sources()
    seed_watchlist()
    result = run_realtime_cycle(include_pizza=include_pizza)
    print("cycle", result)
    print("status", realtime_status())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=int, default=300, help="Seconds between runs. Default 300 seconds.")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--no-pizza", action="store_true")
    args = parser.parse_args()
    if args.once:
        cycle(include_pizza=not args.no_pizza)
        return
    while True:
        cycle(include_pizza=not args.no_pizza)
        print(f"sleeping {args.interval} seconds")
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
