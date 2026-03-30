"""Abstract base classes for storage."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Command = TypeVar('Command')
StoreKey = TypeVar('StoreKey')


class AbstractStoreKeyResolver(ABC, Generic[Command, StoreKey]):
    """ABC for store key resolver by command."""

    @abstractmethod
    def resolve(
        self,
        command: Command,
        prefix: str,
        **kwargs: object,
    ) -> StoreKey:
        """Resolve store key."""
