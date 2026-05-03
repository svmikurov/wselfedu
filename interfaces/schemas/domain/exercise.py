"""Exercise's domain schema interfaces."""

from pydantic import ConfigDict

from contracts.schemas.base import BaseDTO
from contracts.schemas.domain.exercise.fields import (
    DefineField,
    MeanField,
    ProgressValueField,
)
from contracts.schemas.fields import ResourceIdentifierField


class CandidateSchema(
    ResourceIdentifierField,
    DefineField,
    MeanField,
    ProgressValueField,
):
    """Exercise task candidate schema."""

    model_config = ConfigDict(  # type: ignore
        extra='forbid',
        frozen=True,
        from_attributes=True,
    )


class Option(BaseDTO):
    """Test exercise option schema."""

    value: int
    text: str


class ExerciseTaskSchema(BaseDTO):
    """Base exercise task schema."""


class PresentationExerciseTaskSchema(ExerciseTaskSchema):
    """Presentation exercise task schema."""


class TestExerciseTaskSchema(ExerciseTaskSchema):
    """Task exercise tas schema."""
