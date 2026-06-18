"""Abstract base class for infrastructure interface."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')


class AbstractRepository(ABC, Generic[T]):
    """ABC for repository."""

    @abstractmethod
    def add(self, item: T) -> None:
        """Add item."""

    @abstractmethod
    def get(self, key: str) -> T:
        """Get item."""

    @abstractmethod
    def list(self) -> list[T]:
        """Get items."""
