"""Defines clients for storing tasks."""

import uuid

from django.core.cache import cache
from typing_extensions import override
from wse_exercises import TaskT

from services.storage.base import BaseCacheClient


class TaskCache(BaseCacheClient[TaskT]):
    """Django cache client for storing tasks."""

    @staticmethod
    @override
    def set(task: TaskT) -> uuid.UUID:
        """Save object to cache."""
        uid = uuid.uuid4()
        cache.set(uid, task, task.config.ttl)
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
