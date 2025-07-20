"""Defines protocol and abc for cache storage client."""

import uuid
from abc import ABC, abstractmethod
from typing import Protocol, TypeVar

from typing_extensions import override

T = TypeVar('T')


class ICacheUIDClient(Protocol[T]):
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


class CacheUIDClientABC(ICacheUIDClient[T], ABC):
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


class ICacheUserIDClient(Protocol):
    """Protocol for cache storage client interface with user ID."""

    @classmethod
    @abstractmethod
    def set(
        cls,
        obj: object,
        user_id: int,
        prefix: str = '',
        ttl: int | None = None,
    ) -> str:
        """Save an object to the cache."""

    @classmethod
    @abstractmethod
    def get(
        cls,
        user_id: int,
        key: str | None = None,
        prefix: str = '',
    ) -> object:
        """Retrieve an object from the cache."""

    @classmethod
    @abstractmethod
    def pop(
        cls,
        user_id: int,
        key: str | None = None,
        prefix: str = '',
    ) -> object:
        """Remove and return an object from the cache."""

    @classmethod
    @abstractmethod
    def delete(
        cls,
        user_id: int,
        key: str | None = None,
        prefix: str = '',
    ) -> None:
        """Delete an object from the cache."""


class CacheUserIDClientABC(ABC, ICacheUserIDClient):
    """Abstract base class for cache storage client with user ID."""

    @classmethod
    @abstractmethod
    def set(
        cls,
        obj: object,
        user_id: int,
        prefix: str = '',
        ttl: int | None = None,
    ) -> str:
        """Save an object to the cache."""

    @classmethod
    @abstractmethod
    def get(
        cls,
        user_id: int,
        key: str | None = None,
        prefix: str = '',
    ) -> object:
        """Retrieve an object from the cache."""

    @classmethod
    @abstractmethod
    def pop(
        cls,
        user_id: int,
        key: str | None = None,
        prefix: str = '',
    ) -> object:
        """Remove and return an object from the cache."""

    @classmethod
    @abstractmethod
    def delete(
        cls,
        user_id: int,
        key: str | None = None,
        prefix: str = '',
    ) -> None:
        """Delete an object from the cache."""

    @staticmethod
    @abstractmethod
    def _build_key(user_id: int, key: str | None, prefix: str) -> str:
        """Build the cache key."""
