"""Abstract base classes for application layer."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

CommandT = TypeVar('CommandT')
TaskT = TypeVar('TaskT')


class AbstractCreateTaskUseCase(ABC, Generic[CommandT, TaskT]):
    """ABC for create task use case."""

    @abstractmethod
    def execute(self, cmd: CommandT) -> TaskT:
        """Create a task."""
