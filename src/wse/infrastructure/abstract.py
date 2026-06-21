"""Abstract base class for infrastructure interface."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, override

ItemT = TypeVar('ItemT')
KeyT = TypeVar('KeyT')


class AbstractRepository(ABC, Generic[KeyT, ItemT]):
    """ABC for repository."""

    @abstractmethod
    def add(self, item: ItemT) -> None:
        """Add item."""

    @abstractmethod
    def get(self, key: KeyT) -> ItemT:
        """Get item."""

    @abstractmethod
    def list(self) -> list[ItemT]:
        """Get items."""


class AbstractInMemoryRepository(
    AbstractRepository[KeyT, ItemT], Generic[KeyT, ItemT]
):
    """ABC for in memory repository."""

    def __init__(self) -> None:
        super().__init__()
        self._items: set[ItemT] = set()

    @override
    def add(self, item: ItemT) -> None:
        """Add item."""
        self._items.add(item)

    @override
    def list(self) -> list[ItemT]:
        """Get items."""
        return list(self._items)

    @abstractmethod
    def get(self, key: KeyT) -> ItemT:
        """Get item."""
