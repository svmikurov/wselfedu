from datetime import datetime, timezone

from django.core.cache import cache

CACHE_STORAGE_TIME = 10
"""The number of seconds the value should be stored in the cache
(`int`).
"""


def time_cache_key(user_id: int, exercise_type: str) -> str:
    """Key to get start time exercise from cache."""
    cache_key = f'user_{user_id}_exc_{exercise_type}_start_time'
    return cache_key


def set_cache_task_creation_time(user_id: int, exercise_type: str) -> None:
    """Store in cache the date and time of task creation
    for a specific user."""
    key = time_cache_key(user_id, exercise_type)
    data_time_now = datetime.now(tz=timezone.utc)
    cache.set(key, data_time_now, CACHE_STORAGE_TIME)


def get_cache_task_creation_time(user_id: int, exercise_type: str) -> object:
    """Get from cache the date and time of task creation
    for a specific user."""
    key = time_cache_key(user_id, exercise_type)
    return cache.get(key)
