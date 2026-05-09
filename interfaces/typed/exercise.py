"""Exercise data typed dict."""

from contracts.entity.domain.general import ActionTyped, TypedOptionValue
from contracts.enums import ExerciseAction


class TypedCreateTask(
    ActionTyped[ExerciseAction],
):
    """Create task typed request data."""


class TypedCheckTestAnswer(
    ActionTyped[ExerciseAction],
    TypedOptionValue,
):
    """Check test answer typed request data."""
