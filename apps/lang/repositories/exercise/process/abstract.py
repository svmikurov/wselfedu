"""Protocol for process exercise repository."""

from abc import ABC, abstractmethod
from typing import TypeVar, override

from apps.users.models import Person

from .protocol import ProcessExerciseRepositoryProtocol

Command = TypeVar('Command')
Result = TypeVar('Result')


class AbstractProcessExerciseRepository(
    ABC,
    ProcessExerciseRepositoryProtocol[Command, Result],
):
    """ABC for process exercise repository."""

    @override
    @abstractmethod
    def update(self, user: Person, command: Command) -> Result:
        """Update."""
