"""Defines protocols and ABC for storage service."""

import uuid
from abc import ABC, abstractmethod
from typing import Protocol, TypeVar

from typing_extensions import override

T = TypeVar('T')


class ICacheClient(Protocol[T]):
    """Protocol for client interface for storing in cache."""

    @staticmethod
    def set(obj: T) -> uuid.UUID:
        """Save an object to the cache."""

    @staticmethod
    def get(cache_kay: uuid.UUID) -> T:
        """Retrieve an object from the cache."""

    @classmethod
    def pop(cls, cache_kay: uuid.UUID) -> T:
        """Remove and return an object from the cache."""

    @staticmethod
    def delete(cache_kay: uuid.UUID) -> None:
        """Delete an object from the cache."""


class CacheABC(ICacheClient[T], ABC):
    """Abstract base class for storing in cache."""

    @staticmethod
    @abstractmethod
    @override
    def set(obj: T) -> uuid.UUID:
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
