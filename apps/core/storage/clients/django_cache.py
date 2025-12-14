"""Defines client to storage in django cache."""

import uuid
from typing import TypeVar

from django.core.cache import cache
from typing_extensions import override

from .iabc import CacheABC

T = TypeVar('T')


class DjangoCache(CacheABC[T]):
    """Django cache client for storing tasks."""

    DEFAULT_TTL: int = 3600

    def __init__(self, ttl: int | None = None) -> None:
        """Configure the storage."""
        self.ttl = ttl or self.DEFAULT_TTL

    @override
    def set(self, obj: T, ttl: int | None = None) -> uuid.UUID:
        """Save object to cache."""
        cache_key = uuid.uuid4()
        cache.set(cache_key, obj, ttl or self.ttl)
        return cache_key

    @staticmethod
    @override
    def get(cache_key: uuid.UUID) -> T:
        """Retrieve an object from the cache."""
        obj: T = cache.get(cache_key)
        if obj is None:
            raise KeyError(
                f'Object with cache_key {cache_key} not found in cache'
            )
        return obj

    @classmethod
    @override
    def pop(cls, cache_kay: uuid.UUID) -> T:
        """Remove and return an object from the cache."""
        obj = cls.get(cache_kay)
        cls.delete(cache_kay)
        return obj

    @staticmethod
    @override
    def delete(cache_kay: uuid.UUID) -> None:
        """Delete an object from the cache."""
        cache.delete(cache_kay)
