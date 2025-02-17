"""Cache."""

from typing import Any

import redis

from config.constants import REDIS_PARAMS
from users.models import UserApp


class TaskCache:
    """Task data caching."""

    def __init__(self, user: UserApp) -> None:
        """Construct the story."""
        self._user = user

    def save_data(self, mapping: dict[str, Any]) -> None:
        """Save task data."""
        raise NotImplementedError('The method save_data is not implemented')

    def get_data(self) -> dict:
        """Get data."""
        raise NotImplementedError('The method get_data is not implemented')


class RedisTaskCache(TaskCache):
    """Story data in Redis."""

    def __init__(self, user: UserApp) -> None:
        """Construct the story."""
        super().__init__(user)
        self._time = 180
        self._name = str(user)

    def save_data(self, mapping: dict[str, Any]) -> None:
        """Cache the data."""
        conn = redis.Redis(**REDIS_PARAMS)
        conn.hset(self._name, mapping=mapping)
        conn.expire(self._name, self._time)

    def get_data(self) -> dict:
        """Get data from cache."""
        conn = redis.Redis(**REDIS_PARAMS)
        data = conn.hgetall(self._name)
        return data
