"""Defines storage clients to store in the Django cache."""

import uuid

from django.core.cache import cache
from typing_extensions import override
from wse_exercises import TaskT

from ._iabc.icache import CacheUIDClientABC, CacheUserIDClientABC

MAX_TTL = 3600


class TaskDjCache(CacheUIDClientABC[TaskT]):
    """Task store caching client."""

    @override
    def set(self, task: TaskT) -> uuid.UUID:
        """Save an object to the cache."""
        uid = uuid.uuid4()
        ttl = min(task.config.ttl, MAX_TTL)
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


class CacheDjUserID(CacheUserIDClientABC):
    """Cache with user ID into Django cache."""

    @classmethod
    def set(
        cls,
        obj: object,
        user_id: int,
        prefix: str = '',
        ttl: int | None = None,
    ) -> str:
        """Save an object to the cache."""
        ttl = ttl if ttl is not None else MAX_TTL
        key = cls._build_key(user_id, None, prefix)
        cache.set(key, obj, ttl)
        return key

    @classmethod
    def get(
        cls,
        user_id: int,
        key: str | None = None,
        prefix: str = '',
    ) -> object:
        """Retrieve an object from the cache."""
        key = cls._build_key(user_id, key, prefix)
        obj = cache.get(key)
        return obj

    @classmethod
    def pop(
        cls,
        user_id: int,
        key: str | None = None,
        prefix: str = '',
    ) -> object:
        """Remove and return an object from the cache."""
        key = cls._build_key(user_id, key, prefix)
        obj = cls.get(user_id, key, prefix)
        cls.delete(user_id, key, prefix)
        return obj

    @classmethod
    def delete(
        cls,
        user_id: int,
        key: str | None = None,
        prefix: str = '',
    ) -> None:
        """Delete an object from the cache."""
        key = cls._build_key(user_id, key, prefix)
        cache.delete(key)

    @staticmethod
    def _build_key(user_id: int, key: str | None, prefix: str) -> str:
        """Build the cache key."""
        if key is not None:
            return key
        formatted_prefix = '_%s' % prefix if prefix else ''
        return 'user%s_%d' % (formatted_prefix, user_id)
