"""Exercise's domain schema interfaces."""

from pydantic import ConfigDict

from contracts import enums
from contracts.schemas.base import ArbitraryDTO, BaseDTO
from contracts.schemas.domain.exercise.fields import (
    DefineField,
    MeanField,
    ProgressValueField,
)
from contracts.schemas.fields import ResourceIdentifierField


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


class Option(BaseDTO):
    """Test exercise option schema."""

    value: int
    text: str


class PresentationExerciseDomainResult(ArbitraryDTO):
    """Presentation exercise domain result DTO."""

    item: TaskItem
    status: enums.ExerciseStatus
    exercise_kind: enums.ExerciseKind = enums.ExerciseKind.PRESENTATION


class TestExerciseDomainResult(ArbitraryDTO):
    """Test exercise domain result DTO."""

    question_option_value: int
    items: list[TaskItem]
    status: enums.ExerciseStatus
    exercise_kind: enums.ExerciseKind = enums.ExerciseKind.TEST
