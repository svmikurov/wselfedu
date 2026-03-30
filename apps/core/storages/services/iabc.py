"""Defines protocol for task storage interface."""

import uuid
from abc import ABC, abstractmethod
from typing import Generic, Protocol, TypeVar

from typing_extensions import override

T = TypeVar('T')
StoredObject = TypeVar('StoredObject')
Command = TypeVar('Command')


class TaskStorageProto(Protocol[T]):
    """Protocol for task storage interface."""

    def save_task(self, obj: T) -> uuid.UUID:
        """Save task."""

    def retrieve_task(self, uid: uuid.UUID) -> T:
        """Retrieve task."""


class TaskStorageABC(TaskStorageProto[T], ABC):
    """ABC for task storage interface."""

    @abstractmethod
    @override
    def save_task(self, obj: T) -> uuid.UUID:
        """Save task."""

    @abstractmethod
    @override
    def retrieve_task(self, uid: uuid.UUID) -> T:
        """Retrieve task."""


class AbstractCommandStorage(ABC, Generic[Command, StoredObject]):
    """ABC for command related data store."""

    @abstractmethod
    def save(
        self,
        command: Command,
        obj: StoredObject,
        prefix: str,
        ttl: int | None = None,
        **kwargs: object,
    ) -> None:
        """Save data."""

    @abstractmethod
    def retrieve(
        self,
        command: Command,
        prefix: str,
        **kwargs: object,
    ) -> StoredObject:
        """Retrieve data."""


class AbstractUserStorage(ABC, Generic[T]):
    """ABC for user's data store."""

    @abstractmethod
    def save(
        self,
        obj: T,
        user_pk: int,
        prefix: str,
        ttl: int | None = None,
        **kwargs: object,
    ) -> None:
        """Save user's data."""

    @abstractmethod
    def retrieve(self, user_pk: int, prefix: str, **kwargs: object) -> T:
        """Retrieve user's data."""
