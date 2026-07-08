"""Logging and optional error tracking hooks."""
import logging
import os
from logging.handlers import RotatingFileHandler
from config import LOGS_DIR


def setup_logging(name="indomarket", level="INFO"):
    LOGS_DIR.mkdir(exist_ok=True)
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    file_handler = RotatingFileHandler(LOGS_DIR / "indomarket.log", maxBytes=5_000_000, backupCount=5)
    file_handler.setFormatter(fmt)
    console = logging.StreamHandler()
    console.setFormatter(fmt)
    logger.addHandler(file_handler)
    logger.addHandler(console)
    return logger


def setup_sentry_if_configured():
    dsn = os.getenv("SENTRY_DSN", "")
    if not dsn:
        return False
    try:
        import sentry_sdk
        sentry_sdk.init(dsn=dsn, traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.05")))
        return True
    except Exception:
        return False

LOGGER = setup_logging()
