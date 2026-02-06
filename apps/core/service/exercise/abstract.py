"""Abstract base classes for exercise."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from apps.users.models import Person

Case = TypeVar('Case')
CaseMeta = TypeVar('CaseMeta')
ExerciseRequest = TypeVar('ExerciseRequest')
CheckResult = TypeVar('CheckResult')
Explanation = TypeVar('Explanation')


class AbstractExerciseCreate(ABC, Generic[Case]):
    """Abstract base class for create the exercise case."""

    @abstractmethod
    def execute(self, user: Person) -> Case:
        """Create the exercise case."""


class AbstractDetailExerciseCreate(ABC, Generic[Case]):
    """Abstract base class for create the detail exercise case."""

    @abstractmethod
    def execute(self, user: Person, exercise_pk: int) -> Case:
        """Create the exercise case."""


class AbstractExerciseCheck(
    ABC, Generic[CaseMeta, ExerciseRequest, CheckResult]
):
    """Abstract base class for check the user answer."""

    @abstractmethod
    def execute(
        self, case_meta: CaseMeta, data: ExerciseRequest
    ) -> CheckResult:
        """Check the user answer."""


class AbstractMilestone(ABC, Generic[CheckResult, CaseMeta]):
    """Abstract base class for user study milestone update."""

    @abstractmethod
    def execute(
        self, user: Person, result: CheckResult, case_meta: CaseMeta
    ) -> None:
        """Update the user study milestone."""


class AbstractExerciseExplain(
    ABC, Generic[CaseMeta, ExerciseRequest, Explanation]
):
    """Abstract base class for explain the exercise case."""

    @abstractmethod
    def execute(
        self, case_meta: CaseMeta, data: ExerciseRequest
    ) -> Explanation:
        """Explain the exercise case."""


class AbstractExerciseLoop(ABC, Generic[ExerciseRequest, Case, Explanation]):
    """Abstract base class for exercise loop."""

    @abstractmethod
    def execute(
        self, user: Person, data: ExerciseRequest
    ) -> Case | Explanation:
        """Execute the exercise loop."""
