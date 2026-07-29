"""
Rate limiting configuration using SlowAPI (Redis-backed), keyed by client IP.
Applied globally in main.py; individual routes can override limits via
the `@limiter.limit(...)` decorator if finer control is needed.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings

limiter = Limiter(key_func=get_remote_address, storage_uri=settings.REDIS_URL, default_limits=[settings.RATE_LIMIT_DEFAULT])
