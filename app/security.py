"""Authentication, authorization, RBAC, and API rate limiting helpers.

This is intentionally lightweight and local-file based for the starter app.
For production: replace users.json with managed identity/Auth0/Keycloak/Cognito/etc.
"""
import os
import json
import hmac
import time
import hashlib
import secrets
from pathlib import Path
from collections import defaultdict, deque
from typing import Iterable
try:
    from fastapi import Header, HTTPException, Request
except Exception:  # allows local formula/security tests before installing FastAPI
    def Header(default=None):
        return default
    class HTTPException(Exception):
        def __init__(self, status_code=500, detail=""):
            super().__init__(detail)
            self.status_code = status_code
            self.detail = detail
    class Request:  # minimal typing fallback
        client = None
from config import ROOT
from settings import load_settings, get_api_token

USERS_PATH = ROOT / "config" / "users.json"
RBAC_PATH = ROOT / "config" / "rbac.json"

DEFAULT_RBAC = {
    "roles": {
        "admin": ["*"] ,
        "analyst": ["read", "forecast", "report", "export"],
        "operator": ["read", "scrape", "export"],
        "viewer": ["read"]
    }
}

_RATE_BUCKETS = defaultdict(deque)


def hash_password(password: str, salt: str | None = None) -> str:
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 200_000).hex()
    return f"pbkdf2_sha256$200000${salt}${digest}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        algo, rounds, salt, digest = encoded.split("$", 3)
        check = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), int(rounds)).hex()
        return hmac.compare_digest(check, digest)
    except Exception:
        return False


def ensure_default_files():
    if not RBAC_PATH.exists():
        RBAC_PATH.write_text(json.dumps(DEFAULT_RBAC, indent=2), encoding="utf-8")
    if not USERS_PATH.exists():
        # disabled default: user must create admin password intentionally
        USERS_PATH.write_text(json.dumps({"users": []}, indent=2), encoding="utf-8")


def load_users():
    ensure_default_files()
    return json.loads(USERS_PATH.read_text(encoding="utf-8")).get("users", [])


def load_rbac():
    ensure_default_files()
    return json.loads(RBAC_PATH.read_text(encoding="utf-8"))


def authenticate_user(username: str, password: str):
    for user in load_users():
        if user.get("username") == username and user.get("active", True):
            if verify_password(password, user.get("password_hash", "")):
                return user
    return None


def user_has_permission(user: dict, permission: str) -> bool:
    roles = user.get("roles", [])
    rbac = load_rbac().get("roles", {})
    for role in roles:
        perms = rbac.get(role, [])
        if "*" in perms or permission in perms:
            return True
    return False


def require_api_auth(required_permission: str = "read"):
    """FastAPI dependency supporting optional token auth and simple role tokens.

    Modes:
    - If settings.api_token_enabled=false, allow all.
    - If true, accept X-API-Token equal to env token. This maps to admin.
    - Optional future extension: signed JWT/session tokens.
    """
    def _dep(request: Request, x_api_token: str | None = Header(default=None)):
        settings = load_settings()
        if not settings.get("api_token_enabled"):
            return {"username": "anonymous", "roles": ["viewer"]}
        expected = get_api_token(settings)
        if not expected or x_api_token != expected:
            raise HTTPException(status_code=401, detail="Invalid or missing API token")
        user = {"username": "api-token", "roles": ["admin"]}
        if not user_has_permission(user, required_permission):
            raise HTTPException(status_code=403, detail="Permission denied")
        return user
    return _dep


def rate_limit(request: Request, limit: int = 120, window_seconds: int = 60):
    """In-memory rate limiter for single-process deployments.

    For scaled production, replace with Redis/sliding-window limiter at API gateway.
    """
    client = request.client.host if request.client else "unknown"
    now = time.time()
    bucket = _RATE_BUCKETS[client]
    while bucket and bucket[0] <= now - window_seconds:
        bucket.popleft()
    if len(bucket) >= limit:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    bucket.append(now)
    return True
