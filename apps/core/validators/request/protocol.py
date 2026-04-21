"""Protocol for validator interface."""

from typing import Protocol, TypedDict, TypeVar


# REVIEW: Is deprecated&
class ExerciseProcessAction(TypedDict):
    """Exercise process action web data."""

    action: str


# REVIEW: Is deprecated&
class OptionAnswerWebData(
    ExerciseProcessAction,
):
    """Test exercise user's answer request data."""

    option_value: str


RequestData_contra = TypeVar('RequestData_contra', contravariant=True)
Validated_co = TypeVar('Validated_co', covariant=True)


class RequestValidatorProtocol(
    Protocol[RequestData_contra, Validated_co],
):
    """Protocol for request data validator interface."""

    def validate(self, data: RequestData_contra) -> Validated_co:
        """Validate request data."""


# =================================================
# Protocol for validated data
# =================================================


class TestExerciseAnswerProtocol(Protocol):
    """Protocol for test exercise user's answer."""

    option_value: int
