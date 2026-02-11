"""Abstract base classes for exercise services."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from apps.users.models import Person

ExerciseRequest = TypeVar('ExerciseRequest')
ExerciseConditions = TypeVar('ExerciseConditions')
Case = TypeVar('Case')
CaseMeta = TypeVar('CaseMeta')
CheckResult = TypeVar('CheckResult')
Explanation = TypeVar('Explanation')

# -----------------------------------------------
# Create
# -----------------------------------------------


class AbstractExerciseCreate(ABC, Generic[Case]):
    """ABC for service to create the exercise case."""

    @abstractmethod
    def execute(self, user: Person) -> Case:
        """Create the exercise case."""


class AbstractDetailExerciseCreate(ABC, Generic[Case]):
    """ABC for service to create the detail exercise case."""

    @abstractmethod
    def execute(self, user: Person, exercise_pk: int) -> Case:
        """Create the exercise case."""


class AbstractConditionsExerciseCreate(ABC, Generic[ExerciseConditions, Case]):
    """ABC for service to create exercise by conditions."""

    @abstractmethod
    def execute(self, conditions: ExerciseConditions) -> Case:
        """Create exercise case."""


# -----------------------------------------------
# Check
# -----------------------------------------------


class AbstractExerciseCheck(
    ABC, Generic[CaseMeta, ExerciseRequest, CheckResult]
):
    """ABC for service to check the user answer."""

    @abstractmethod
    def execute(
        self, case_meta: CaseMeta, data: ExerciseRequest
    ) -> CheckResult:
        """Check the user answer."""


# -----------------------------------------------
# Milestone
# -----------------------------------------------


class AbstractMilestone(ABC, Generic[CheckResult, CaseMeta]):
    """ABC for user study milestone update service."""

    @abstractmethod
    def execute(
        self, user: Person, result: CheckResult, case_meta: CaseMeta
    ) -> None:
        """Update the user study milestone."""


# -----------------------------------------------
# Explain
# -----------------------------------------------


class AbstractExerciseExplain(
    ABC, Generic[CaseMeta, ExerciseRequest, Explanation]
):
    """ABC for service to explain the exercise case."""

    @abstractmethod
    def execute(
        self, case_meta: CaseMeta, data: ExerciseRequest
    ) -> Explanation:
        """Explain the exercise case."""


# -----------------------------------------------
# Exercise loop
# -----------------------------------------------


class AbstractExerciseLoop(ABC, Generic[ExerciseRequest, Case, Explanation]):
    """ABC for exercise loop service."""

    @abstractmethod
    def execute(
        self, user: Person, data: ExerciseRequest
    ) -> Case | Explanation:
        """Execute the exercise loop."""
