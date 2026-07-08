"""Tiny TTL cache abstraction. Replace with Redis for production."""
import time
from functools import wraps

_CACHE = {}


def ttl_cache(seconds=60):
    def deco(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            key = (fn.__name__, repr(args), repr(sorted(kwargs.items())))
            now = time.time()
            if key in _CACHE:
                expires, value = _CACHE[key]
                if now < expires:
                    return value
            value = fn(*args, **kwargs)
            _CACHE[key] = (now + seconds, value)
            return value
        return wrapper
    return deco


def clear_cache():
    _CACHE.clear()
