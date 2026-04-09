"""Protocol for presentation exercise interface."""

from typing import Protocol, TypeVar

from ..protocol import (
    Candidate,
    HasAnswerText,
    HasExerciseStatus,
    HasOption,
    HasProgressValue,
    HasQuestionText,
)

OptionT = TypeVar('OptionT', bound=Candidate)


class PresentationCreateResultProtocol(
    HasOption[OptionT],
    Protocol,
):
    """Presentation exercise create domain result DTO interface."""


class PresentationTaskProtocol(
    HasExerciseStatus,
    HasQuestionText,
    HasAnswerText,
    HasProgressValue,
    Protocol,
):
    """Presentation exercise case DTO interface."""
