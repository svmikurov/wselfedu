"""Repository."""

from typing import TypeVar, override

from wse.domain.protocols import HasIdentifier, HasSessionIdentifier

from .abstract import AbstractInMemoryRepository

ItemT = TypeVar('ItemT')
KeyT = TypeVar('KeyT')


class InMemoryLearnableRepository(
    AbstractInMemoryRepository[int, HasIdentifier]
):
    """In memory learnable repository."""

    @override
    def get(self, key: int) -> HasIdentifier:
        """Get item."""
        return next(item for item in self._items if item.pk == key)


class InMemoryTaskRepository(
    AbstractInMemoryRepository[str, HasSessionIdentifier]
):
    """In memory task repository."""

    @override
    def get(self, key: str) -> HasSessionIdentifier:
        """Get item."""
        return next(item for item in self._items if item.session_id == key)
