"""Defines client to storage in django cache."""

import uuid
from typing import TypeVar

from django.core.cache import cache
from typing_extensions import override

from .iabc import CacheABC

T = TypeVar('T')


class DjangoCache(CacheABC[T]):
    """Django cache client for storing tasks."""

    @staticmethod
    @override
    def set(obj: T, ttl: int | None = None) -> uuid.UUID:
        """Save object to cache."""
        uid = uuid.uuid4()
        cache.set(uid, obj, ttl)
        return uid

    @staticmethod
    @override
    def get(uid: uuid.UUID) -> T:
        """Retrieve an object from the cache."""
        obj: T = cache.get(uid)
        if obj is None:
            raise KeyError(f'Object with uid {uid} not found in cache')
        return obj

    @classmethod
    @override
    def pop(cls, uid: uuid.UUID) -> T:
        """Remove and return an object from the cache."""
        obj = cls.get(uid)
        cls.delete(uid)
        return obj

    @staticmethod
    @override
    def delete(uid: uuid.UUID) -> None:
        """Delete an object from the cache."""
        cache.delete(uid)
