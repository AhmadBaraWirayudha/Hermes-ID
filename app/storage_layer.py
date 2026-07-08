"""Storage abstraction layer.

Current app uses SQLite via db.py. This module adds production-ready helpers for
DATABASE_URL-based SQLAlchemy engines while preserving SQLite compatibility.
"""
import os
from contextlib import contextmanager
from pathlib import Path
from config import DB_PATH


def get_database_url():
    return os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")


def get_sqlalchemy_engine():
    try:
        from sqlalchemy import create_engine
    except Exception as exc:
        raise ImportError("SQLAlchemy is required for storage_layer. Install requirements.txt") from exc
    url = get_database_url()
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    return create_engine(url, pool_pre_ping=True, future=True, connect_args=connect_args)


@contextmanager
def engine_connection():
    engine = get_sqlalchemy_engine()
    with engine.begin() as conn:
        yield conn


def storage_backend_name():
    url = get_database_url()
    if url.startswith("postgres"):
        return "postgresql"
    if url.startswith("sqlite"):
        return "sqlite"
    return url.split(":", 1)[0]


def object_storage_config():
    """Return object-storage config for future raw/report storage.

    Supported envs are intentionally provider-neutral.
    """
    return {
        "provider": os.getenv("OBJECT_STORAGE_PROVIDER", "local"),
        "bucket": os.getenv("OBJECT_STORAGE_BUCKET", ""),
        "endpoint_url": os.getenv("OBJECT_STORAGE_ENDPOINT_URL", ""),
        "region": os.getenv("OBJECT_STORAGE_REGION", ""),
        "local_root": os.getenv("OBJECT_STORAGE_LOCAL_ROOT", "data"),
    }
