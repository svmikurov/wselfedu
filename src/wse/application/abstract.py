"""Abstract base classes for use case."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from wse.domain.protocols import EventProto, ExerciseCommandProto


TaskT = TypeVar('TaskT')
ResultT = TypeVar('ResultT')
CheckT = TypeVar('CheckT')


class AbstractCreateTaskUseCase(ABC, Generic[ResultT]):
    """ABC for create task use case."""

    @abstractmethod
    def execute(self) -> ResultT:
        """Create the task."""


class AbstractCheckAnswerUseCase(ABC, Generic[CheckT, ResultT]):
    """ABC for check user answer use case."""

    @abstractmethod
    def execute(self, spec: CheckT) -> ResultT:
        """Check the user answer."""


class AbstractExerciseUseCase(ABC):
    """ABC for exercise action execute use case."""

    @abstractmethod
    def execute(
        self,
        command: ExerciseCommandProto,
    ) -> EventProto:
        """Execute exercise command action."""
