"""Abstract base classes for exercise services."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar, override

from .protocol import CreateExerciseProtocol

if TYPE_CHECKING:
    from apps.users.models import Person

# Start exercise conditions
CommandDataT = TypeVar('CommandDataT')
ExerciseParametersT = TypeVar('ExerciseParametersT')

# Current exercise case data
CaseT = TypeVar('CaseT')
TaskT = TypeVar('TaskT')
CaseMeta = TypeVar('CaseMeta')

# Current exercise case solve
UserAnswerT = TypeVar('UserAnswerT')
CheckResultT = TypeVar('CheckResultT')
ExplanationT = TypeVar('ExplanationT')


# =================================================
# Create
# =================================================


class AbstractCreateExerciseService(
    ABC,
    CreateExerciseProtocol[ExerciseParametersT, TaskT],
):
    """ABC for service to create the exercise case."""

    @override
    @abstractmethod
    def execute(
        self,
        user: Person,
        spec: ExerciseParametersT,
    ) -> TaskT:
        """Create the exercise case."""


# =================================================
# Check
# =================================================


class AbstractCheckExerciseService(
    ABC,
    Generic[UserAnswerT, CaseMeta, CheckResultT],
):
    """ABC for service to check the user answer."""

    @abstractmethod
    def execute(
        self,
        answer: UserAnswerT,
        case_meta: CaseMeta,
    ) -> CheckResultT:
        """Check the user answer."""


# =================================================
# Milestone
# =================================================


class AbstractMilestoneService(
    ABC,
    Generic[CommandDataT, CaseMeta, CheckResultT, ExerciseParametersT],
):
    """ABC for user study milestone update service."""

    @abstractmethod
    def execute(
        self,
        command: CommandDataT,
        meta: CaseMeta,
        result: CheckResultT,
        exercise_parameters: ExerciseParametersT,
    ) -> None:
        """Update the user study milestone."""


# =================================================
# Explain
# =================================================


class AbstractExplainExerciseService(
    ABC,
    Generic[CommandDataT, CaseMeta, ExplanationT],
):
    """ABC for service to explain the exercise case."""

    @abstractmethod
    def execute(
        self,
        command: CommandDataT,
        case_meta: CaseMeta,
    ) -> ExplanationT:
        """Explain the exercise case."""
