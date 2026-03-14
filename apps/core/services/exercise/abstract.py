"""Abstract base classes for exercise services."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from apps.users.models import Person

UserAnswer = TypeVar('UserAnswer')
Conditions = TypeVar('Conditions')

UuidSchema = TypeVar('UuidSchema')
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


class AbstractUuidExerciseCreate(ABC, Generic[UuidSchema, Case]):
    """ABC for service to create exercise by stored UUID."""

    @abstractmethod
    def execute(self, data: UuidSchema) -> Case:
        """Create exercise case."""


class AbstractRegularExerciseCreate(ABC, Generic[Conditions, Case]):
    """ABC for service to create exercise by stored UUID."""

    @abstractmethod
    def execute(self, conditions: Conditions) -> Case:
        """Create exercise case."""


# -----------------------------------------------
# Check
# -----------------------------------------------


class AbstractExerciseCheck(ABC, Generic[UserAnswer, CaseMeta, CheckResult]):
    """ABC for service to check the user answer."""

    @abstractmethod
    def execute(self, answer: UserAnswer, case_meta: CaseMeta) -> CheckResult:
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


class AbstractStudentMilestone(ABC, Generic[CheckResult, CaseMeta]):
    """ABC for user study milestone update service."""

    @abstractmethod
    def execute(
        self,
        user: Person,
        result: CheckResult,
        case_meta: CaseMeta,
        **kwargs: object,
    ) -> None:
        """Update the user study milestone."""


# -----------------------------------------------
# Explain
# -----------------------------------------------


class AbstractExerciseExplain(ABC, Generic[UserAnswer, CaseMeta, Explanation]):
    """ABC for service to explain the exercise case."""

    @abstractmethod
    def execute(self, answer: UserAnswer, case_meta: CaseMeta) -> Explanation:
        """Explain the exercise case."""


# -----------------------------------------------
# Exercise performing
# -----------------------------------------------


class StartAbstractExercise(ABC, Generic[Conditions, Case]):
    """ABC for start exercise service."""

    @abstractmethod
    def execute(self, user: Person, schema: Conditions) -> Case:
        """Start exercise."""


class AbstractExerciseLoop(ABC, Generic[Conditions, Case, Explanation]):
    """ABC for exercise loop service."""

    @abstractmethod
    def execute(self, user: Person, schema: Conditions) -> Case | Explanation:
        """Execute the exercise loop."""
