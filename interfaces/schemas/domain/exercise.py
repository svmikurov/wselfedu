"""Exercise's domain schema interfaces."""

from contracts.schemas.base import BaseDTO


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
