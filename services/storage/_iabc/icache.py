"""Defines protocol and abc for cache storage client."""

import uuid
from abc import ABC, abstractmethod
from typing import Protocol, TypeVar

from typing_extensions import override

T = TypeVar('T')


class ICacheClient(Protocol[T]):
    """Protocol for cache storage client interface."""

    def set(self, obj: T) -> uuid.UUID:
        """Save an object to the cache."""

    @staticmethod
    def get(uid: uuid.UUID) -> T:
        """Retrieve an object from the cache."""

    @staticmethod
    def pop(uid: uuid.UUID) -> T:
        """Remove and return an object from the cache."""

    @staticmethod
    def delete(uid: uuid.UUID) -> None:
        """Delete an object from the cache."""


class CacheClientABC(ICacheClient[T], ABC):
    """Abstract base class for cache storage client."""

    @abstractmethod
    @override
    def set(self, obj: T) -> uuid.UUID:
        """Save an object to the cache."""

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
