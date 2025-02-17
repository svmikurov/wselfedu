"""Storing data on a Redis server."""

from datetime import datetime, timezone

import redis
from django.core.cache import cache

from config.constants import CACHE_STORAGE_TIME, REDIS_PARAMS


def set_cache_dict(name: str, mapping: dict) -> None:
    """Set the mapping to cache."""
    conn = redis.Redis(**REDIS_PARAMS)
    conn.hset(name, mapping=mapping)


def get_cache_dict(name: str) -> dict:
    """Get the mapping from cache."""
    conn = redis.Redis(**REDIS_PARAMS)
    mapping = conn.hgetall(name)
    return mapping


def time_cache_key(user_id: int, exercise: str) -> str:
    """Key to get start time exercise from cache."""
    cache_key = f'user_{user_id}_exc_{exercise}_start_time'
    return cache_key


def set_cache_task_creation_time(user_id: int, exercise: str) -> None:
    """Store in cache the data for a specific user."""
    key = time_cache_key(user_id, exercise)
    data_time_now = datetime.now(tz=timezone.utc)
    cache.set(key, data_time_now, CACHE_STORAGE_TIME)


def get_cache_task_creation_time(user_id: int, exercise: str) -> object:
    """Get from cache the data for a specific user."""
    key = time_cache_key(user_id, exercise)
    return cache.get(key)
