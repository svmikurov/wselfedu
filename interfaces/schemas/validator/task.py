"""Create task WEB exercise interfaces."""

from contracts.schemas.domain.exercise.fields import ExerciseActionField


class CreateTaskWebValidated(
    ExerciseActionField,
):
    """Create task WEB request validated data."""
