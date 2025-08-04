"""Defines protocols for storage interfaces."""

import uuid
from typing import Protocol, TypeVar

T = TypeVar('T')


class ICacheClient(Protocol[T]):
    """Protocol for client interface for storing in cache."""

    @staticmethod
    def set(obj: T) -> uuid.UUID:
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
