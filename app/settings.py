"""Application settings loader/saver."""
import os
import json
from pathlib import Path
from config import ROOT

SETTINGS_PATH = ROOT / "config" / "settings.json"

DEFAULT_SETTINGS = {
    "language": "en",
    "default_region": "Indonesia",
    "default_currency": "IDR",
    "scrape_delay_seconds": 1.0,
    "respect_robots": True,
    "api_token_enabled": False,
    "api_token_env": "INDOMARKET_API_TOKEN",
    "webhook_url": "",
    "smtp": {
        "enabled": False,
        "host": "",
        "port": 587,
        "username": "",
        "password_env": "INDOMARKET_SMTP_PASSWORD",
        "from_email": "",
        "to_email": ""
    }
}


def load_settings():
    if not SETTINGS_PATH.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()
    try:
        loaded = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
        return _deep_merge(DEFAULT_SETTINGS.copy(), loaded)
    except Exception:
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_PATH.write_text(json.dumps(settings, indent=2, ensure_ascii=False), encoding="utf-8")
    return SETTINGS_PATH


def _deep_merge(base, override):
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            base[k] = _deep_merge(base[k], v)
        else:
            base[k] = v
    return base


def get_api_token(settings=None):
    settings = settings or load_settings()
    return os.getenv(settings.get("api_token_env", "INDOMARKET_API_TOKEN"), "")
