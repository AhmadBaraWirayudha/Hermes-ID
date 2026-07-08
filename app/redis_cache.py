"""Redis-ready cache abstraction with in-memory fallback."""
import os
import json
import time

_MEMORY = {}


def _redis_client():
    url = os.getenv("REDIS_URL", "")
    if not url:
        return None
    try:
        import redis
        return redis.Redis.from_url(url, decode_responses=True)
    except Exception:
        return None


def cache_get(key):
    r = _redis_client()
    if r:
        raw = r.get(key)
        return json.loads(raw) if raw else None
    item = _MEMORY.get(key)
    if not item:
        return None
    expires, value = item
    if time.time() > expires:
        _MEMORY.pop(key, None)
        return None
    return value


def cache_set(key, value, ttl=60):
    r = _redis_client()
    if r:
        r.setex(key, ttl, json.dumps(value, default=str))
    else:
        _MEMORY[key] = (time.time() + ttl, value)
    return True


def cache_delete(key):
    r = _redis_client()
    if r:
        r.delete(key)
    else:
        _MEMORY.pop(key, None)
