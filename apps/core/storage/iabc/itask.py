"""Defines protocol for task storage interface."""

import uuid
from typing import Protocol, TypeVar

T = TypeVar('T')


class ITaskStorage(Protocol[T]):
    """Protocol for task storage interface."""

    def save_task(self, obj: T) -> uuid.UUID:
        """Save task."""

    def retrieve_task(self, uid: uuid.UUID) -> T:
        """Retrieve task."""
