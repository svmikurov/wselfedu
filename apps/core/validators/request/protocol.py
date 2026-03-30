"""Protocol for validator interface."""

from typing import Protocol, TypedDict

from apps.core.domains.exercise.enums import ExerciseProcessEnum

# =================================================
# Protocol for data validate
# =================================================


class ExerciseProcessAction(TypedDict):
    """Exercise process action web data."""

    action: ExerciseProcessEnum


class OptionAnswerWebData(
    ExerciseProcessAction,
):
    """Test exercise user's answer request data."""

    option_value: str


# =================================================
# Protocol for validated data
# =================================================


class TestExerciseAnswerProtocol(Protocol):
    """Protocol for test exercise user's answer."""

    option_value: int
