"""Exercise's domain schema interfaces."""

from pydantic import ConfigDict

from contracts import enums
from contracts.schemas.base import ArbitraryDTO
from contracts.schemas.domain.exercise.fields import (
    DefineField,
    IsCorrectAnswerField,
    MeanField,
    ProgressValueField,
)
from contracts.schemas.fields import ResourceIdentifierField

# =================================================
# Task
# =================================================


class TaskItem(
    ResourceIdentifierField,
    DefineField,
    MeanField,
    ProgressValueField,
):
    """Exercise task item schema."""

    model_config = ConfigDict(  # type: ignore
        extra='forbid',
        frozen=True,
        from_attributes=True,
    )


# =================================================
# Exercise domain result
# =================================================


class PresentationExerciseDomainResult(ArbitraryDTO):
    """Presentation exercise domain result DTO."""

    item: TaskItem
    status: enums.ExerciseStatus
    exercise_kind: enums.ExerciseKind = enums.ExerciseKind.PRESENTATION


class TestExerciseDomainResult(ArbitraryDTO):
    """Test exercise domain result DTO."""

    __test__ = False

    question_option_value: int
    items: list[TaskItem]
    status: enums.ExerciseStatus
    exercise_kind: enums.ExerciseKind = enums.ExerciseKind.TEST


# =================================================
# Task answer check result
# =================================================


class CheckTaskResult(IsCorrectAnswerField):
    """Check task result schema."""

    is_correct: bool
