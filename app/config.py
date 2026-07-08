from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
MODELS_DIR = ROOT / "models"
LOGS_DIR = ROOT / "logs"
DB_PATH = ROOT / "data" / "indomarket.sqlite"
TIMEZONE = "Asia/Jakarta"
DEFAULT_CURRENCY = "IDR"

for p in [DATA_RAW, DATA_PROCESSED, MODELS_DIR, LOGS_DIR]:
    p.mkdir(parents=True, exist_ok=True)
