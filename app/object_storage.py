"""Object storage helper with local filesystem fallback.

Production can configure S3-compatible storage via environment variables.
For local S3-compatible testing use MinIO from podman-compose.storage.yml.
"""
import os
from pathlib import Path
from config import ROOT
from storage_layer import object_storage_config


def put_object(local_path, key=None):
    cfg = object_storage_config()
    local_path = Path(local_path)
    key = key or local_path.name
    if cfg["provider"] == "local":
        dest_root = ROOT / cfg.get("local_root", "data") / "objects"
        dest_root.mkdir(parents=True, exist_ok=True)
        dest = dest_root / key
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(local_path.read_bytes())
        return str(dest)
    if cfg["provider"] in ["s3", "minio"]:
        try:
            import boto3
        except Exception as exc:
            raise ImportError("boto3 required for S3/MinIO object storage") from exc
        session = boto3.session.Session(region_name=cfg.get("region") or None)
        client = session.client("s3", endpoint_url=cfg.get("endpoint_url") or None)
        client.upload_file(str(local_path), cfg["bucket"], key)
        return f"s3://{cfg['bucket']}/{key}"
    raise ValueError(f"Unsupported object storage provider: {cfg['provider']}")


def get_object_uri(key):
    cfg = object_storage_config()
    if cfg["provider"] == "local":
        return str(ROOT / cfg.get("local_root", "data") / "objects" / key)
    return f"s3://{cfg['bucket']}/{key}"
