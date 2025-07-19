"""Defines storage clients to store in the Django cache."""

import uuid

from django.core.cache import cache
from typing_extensions import override
from wse_exercises import TaskT

from ._iabc.icache import CacheClientABC


class TaskDjCache(CacheClientABC[TaskT]):
    """Task store caching client."""

    MAX_TTL = 3600

    @override
    def set(self, task: TaskT) -> uuid.UUID:
        """Save an object to the cache."""
        uid = uuid.uuid4()
        ttl = min(task.config.ttl, self.MAX_TTL)
        cache.set(uid, task, ttl)
        return uid

    @staticmethod
    @override
    def get(uid: uuid.UUID) -> TaskT:
        """Retrieve an object from the cache."""
        task: TaskT = cache.get(uid)
        if task is None:
            raise KeyError(f'Task with uid {uid} not found in cache')
        return task

    @classmethod
    @override
    def pop(cls, uid: uuid.UUID) -> TaskT:
        """Remove and return an object from the cache."""
        task = cls.get(uid)
        cls.delete(uid)
        return task

    @staticmethod
    @override
    def delete(uid: uuid.UUID) -> None:
        """Delete an object from the cache."""
        cache.delete(uid)
