"""Repository."""

from typing import Generic, TypeVar, override

from wse.domain.protocols import HasSessionIdentifier

from .abstract import AbstractRepository

T = TypeVar('T', bound=HasSessionIdentifier)


class InMemoryRepository(AbstractRepository[T], Generic[T]):
    """In memory repository."""

    def __init__(self) -> None:
        super().__init__()
        self._items: set[T] = set()

    @override
    def add(self, item: T) -> None:
        """Add item."""
        self._items.add(item)

    @override
    def get(self, key: str) -> T:
        """Get item."""
        return next(item for item in self._items if item.session_id == key)

    @override
    def list(self) -> list[T]:
        """Get items."""
        return list(self._items)
