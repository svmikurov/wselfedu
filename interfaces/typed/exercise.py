"""Exercise data typed dict."""

from ports.contract.entity.domain.general import ActionTyped, TypedOptionValue
from ports.contract.enums import ExerciseAction


class TypedCreateTask(
    ActionTyped[ExerciseAction],
):
    """Create task typed request data."""


class TypedCheckTestAnswer(
    ActionTyped[ExerciseAction],
    TypedOptionValue,
):
    """Check test answer typed request data."""
