"""Storing data on a Redis server."""

from datetime import datetime, timezone

import redis
from django.core.cache import cache

from config.constants import REDIS_PARAMS, CACHE_STORAGE_TIME


def set_cache_dict(name: str, mapping: dict) -> None:
    """Set the mapping to cache."""
    conn = redis.Redis(**REDIS_PARAMS)
    conn.hset(name, mapping=mapping)


def get_cache_dict(name: str) -> dict:
    """Get the mapping from cache."""
    conn = redis.Redis(**REDIS_PARAMS)
    mapping = conn.hgetall(name)
    return mapping


def time_cache_key(user_id: int, exercise_type: str) -> str:
    """Key to get start time exercise from cache."""
    cache_key = f'user_{user_id}_exc_{exercise_type}_start_time'
    return cache_key


def set_cache_task_creation_time(user_id: int, exercise_type: str) -> None:
    """Store in cache the data for a specific user."""
    key = time_cache_key(user_id, exercise_type)
    data_time_now = datetime.now(tz=timezone.utc)
    cache.set(key, data_time_now, CACHE_STORAGE_TIME)


def get_cache_task_creation_time(user_id: int, exercise_type: str) -> object:
    """Get from cache the data for a specific user."""
    key = time_cache_key(user_id, exercise_type)
    return cache.get(key)
