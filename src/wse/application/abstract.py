"""Abstract base classes for application layer."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

CommandT = TypeVar('CommandT')
ResultT = TypeVar('ResultT')


class AbstractUseCase(ABC, Generic[CommandT, ResultT]):
    """ABC for use case."""

    @abstractmethod
    def execute(self, cmd: CommandT) -> ResultT:
        """Execute a command."""
