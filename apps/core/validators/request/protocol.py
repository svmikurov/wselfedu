"""Protocol for validator interface."""

from typing import Protocol, TypedDict

# =================================================
# Protocol for data to validate
# =================================================


class TestExerciseAnswerRequestData(TypedDict):
    """Test exercise user's answer request data."""

    option_value: str


# =================================================
# Protocol for validated data
# =================================================


class TestExerciseAnswerProtocol(Protocol):
    """Protocol for test exercise user's answer."""

    option_value: int
