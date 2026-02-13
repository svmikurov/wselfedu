"""Defines protocols and ABC for storage service."""

import uuid
from abc import ABC, abstractmethod
from typing import Generic, Protocol, TypeVar

from typing_extensions import override

T = TypeVar('T')


class StorageClient(Protocol[T]):
    """Protocol for client interface for storing."""

    def set(self, obj: T) -> uuid.UUID:
        """Save an object to the storage."""

    @staticmethod
    def get(cache_kay: uuid.UUID) -> T:
        """Retrieve an object from the storage."""

    @classmethod
    def pop(cls, cache_kay: uuid.UUID) -> T:
        """Remove and return an object from the storage."""

    @staticmethod
    def delete(cache_kay: uuid.UUID) -> None:
        """Delete an object from the storage."""


class CacheABC(StorageClient[T], ABC):
    """Abstract base class for storing in cache."""

    @abstractmethod
    @override
    def set(self, obj: T) -> uuid.UUID:
        """Save object to cache."""

    @staticmethod
    @abstractmethod
    @override
    def get(cache_kay: uuid.UUID) -> T:
        """Retrieve an object from the cache."""

    @classmethod
    @abstractmethod
    @override
    def pop(cls, cache_kay: uuid.UUID) -> T:
        """Remove and return an object from the cache."""

    @staticmethod
    @abstractmethod
    @override
    def delete(cache_kay: uuid.UUID) -> None:
        """Delete an object from the cache."""


class KeyCacheABC(ABC, Generic[T]):
    """Abstract base class for storing in cache."""

    @abstractmethod
    def set(self, obj: T, cache_key: str, ttl: int | None) -> None:
        """Save object to cache."""

    @staticmethod
    @abstractmethod
    def get(cache_key: str) -> T:
        """Retrieve an object from the cache."""

    @classmethod
    @abstractmethod
    def pop(cls, cache_key: str) -> T:
        """Remove and return an object from the cache."""

    @staticmethod
    @abstractmethod
    def delete(cache_key: str) -> None:
        """Delete an object from the cache."""
