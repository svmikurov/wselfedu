"""Defines abstract base classes for storage services."""

import uuid
from abc import ABC, abstractmethod

from typing_extensions import override

from .iclient import ICacheClient, T


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
    def get(uid: uuid.UUID) -> T:
        """Retrieve an object from the cache."""

    @staticmethod
    @abstractmethod
    @override
    def pop(uid: uuid.UUID) -> T:
        """Remove and return an object from the cache."""

    @staticmethod
    @abstractmethod
    @override
    def delete(uid: uuid.UUID) -> None:
        """Delete an object from the cache."""
