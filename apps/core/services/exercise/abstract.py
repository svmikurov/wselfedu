"""Abstract base classes for exercise services."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

from .protocol import CreateExerciseProtocol

if TYPE_CHECKING:
    from apps.users.models import Person

# Start exercise conditions
CommandData = TypeVar('CommandData')
ExerciseParameters = TypeVar('ExerciseParameters')

# Current exercise case data
Case = TypeVar('Case')
CaseMeta = TypeVar('CaseMeta')

# Current exercise case solve
UserAnswer = TypeVar('UserAnswer')
CheckResult = TypeVar('CheckResult')
Explanation = TypeVar('Explanation')


# =================================================
# Create
# =================================================


class AbstractCreateExerciseService(
    ABC,
    CreateExerciseProtocol[ExerciseParameters, tuple[Case, CaseMeta]],
):
    """ABC for service to create the exercise case."""

    @abstractmethod
    def execute(
        self,
        parameters: ExerciseParameters,
        user: Person,
    ) -> tuple[Case, CaseMeta]:
        """Create the exercise case."""


# =================================================
# Check
# =================================================


class AbstractCheckExerciseService(
    ABC,
    Generic[UserAnswer, CaseMeta, CheckResult],
):
    """ABC for service to check the user answer."""

    @abstractmethod
    def execute(
        self,
        answer: UserAnswer,
        case_meta: CaseMeta,
    ) -> CheckResult:
        """Check the user answer."""


# =================================================
# Milestone
# =================================================


class AbstractMilestoneService(
    ABC,
    Generic[CommandData, CaseMeta, CheckResult, ExerciseParameters],
):
    """ABC for user study milestone update service."""

    @abstractmethod
    def execute(
        self,
        command: CommandData,
        meta: CaseMeta,
        result: CheckResult,
        exercise_parameters: ExerciseParameters,
    ) -> None:
        """Update the user study milestone."""


# =================================================
# Explain
# =================================================


class AbstractExplainExerciseService(
    ABC,
    Generic[UserAnswer, CaseMeta, Explanation],
):
    """ABC for service to explain the exercise case."""

    @abstractmethod
    def execute(
        self,
        answer: UserAnswer,
        case_meta: CaseMeta,
    ) -> Explanation:
        """Explain the exercise case."""
