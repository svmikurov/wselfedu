"""Contracts for exercise parameters."""

from typing import Protocol, TypeVar

from ports.contract.enums import ExerciseStatus
from ports.contract.entity.general import HasStatus

T = TypeVar('T')


# =================================================
# Conditions
# =================================================


class HasPeriod(Protocol):
    """Protocol for has *start_period*, *end_period* interface."""

    start_period: int | None
    end_period: int | None


class HasProgress(Protocol):
    """Protocol for has progress interface."""

    is_study: bool = True
    is_repeat: bool = True
    is_examine: bool = True
    is_know: bool = True


class HasProgressValue(Protocol):
    """Protocol for has progress value integer field."""

    progress_value: int


# =================================================
# Configuration
# =================================================


class HasDisplayOrder(Protocol[T]):
    """Protocol for item display order object interface."""

    display_order: T


class HasItemCount(Protocol):
    """Protocol for item count object interface."""

    item_count: int | None


class HasOptionCount(Protocol):
    """Protocol for item option count object interface."""

    option_count: int


# =================================================
# Settings
# =================================================


class HasTimeout(Protocol):
    """Protocol for exercise phase timeout interface."""

    question_timeout: int | None = None
    answer_timeout: int | None = None


class HasExerciseStatus(
    HasStatus[ExerciseStatus],
    Protocol,
):
    """Protocol for has exercise status interface."""
