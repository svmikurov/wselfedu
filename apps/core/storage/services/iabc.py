"""Defines protocol for task storage interface."""

import uuid
from abc import ABC, abstractmethod
from typing import Protocol, TypeVar

from typing_extensions import override

T = TypeVar('T')


class TaskStorageProto(Protocol[T]):
    """Protocol for task storage interface."""

    def save_task(self, obj: T) -> uuid.UUID:
        """Save task."""

    def retrieve_task(self, uid: uuid.UUID) -> T:
        """Retrieve task."""


class TaskStorageABC(TaskStorageProto[T], ABC):
    """Protocol for task storage interface."""

    @abstractmethod
    @override
    def save_task(self, obj: T) -> uuid.UUID:
        """Save task."""

    @abstractmethod
    @override
    def retrieve_task(self, uid: uuid.UUID) -> T:
        """Retrieve task."""
