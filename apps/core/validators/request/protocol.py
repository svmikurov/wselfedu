"""Protocol for validator interface."""

from typing import Protocol, TypedDict

from apps.core.domains.exercise.enums import ExerciseProcessEnum


# REVIEW: Is deprecated&
class ExerciseProcessAction(TypedDict):
    """Exercise process action web data."""

    action: ExerciseProcessEnum


# REVIEW: Is deprecated&
class OptionAnswerWebData(
    ExerciseProcessAction,
):
    """Test exercise user's answer request data."""

    option_value: str


# =================================================
# Protocol for data validate
# =================================================


# =================================================
# Protocol for validated data
# =================================================


class TestExerciseAnswerProtocol(Protocol):
    """Protocol for test exercise user's answer."""

    option_value: int
