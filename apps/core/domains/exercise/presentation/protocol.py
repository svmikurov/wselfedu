"""Protocol for presentation exercise interface."""

from typing import Protocol, TypeVar

from interfaces.protocols.domain.exercise import (
    Candidate,
    HasAnswerText,
    HasExerciseStatus,
    HasProgressValue,
    HasQuestionText,
)

from ..protocol import (
    HasCase,
    HasOption,
    HasOptionValue,
)

OptionT = TypeVar('OptionT', bound=Candidate)


# DEPRECATED: Remove `PresentationCreateResultProtocol`
class PresentationCreateResultProtocol(
    HasOption[Candidate],
    Protocol,
):
    """Presentation exercise create domain result DTO interface."""


class _Candidate(
    Candidate,
    Protocol,
):
    """Presentation exercise candidate."""

    progress: int


class PresentationCaseProtocol(
    HasOptionValue,
    HasOption[_Candidate],
    Protocol,
):
    """Presentation exercise case DTO interface."""


class PresentationDomainResultProtocol(
    HasExerciseStatus,
    HasCase[PresentationCaseProtocol],
    Protocol,
):
    """Presentation exercise domain result DTO interface."""


class PresentationTaskProtocol(
    HasExerciseStatus,
    HasQuestionText,
    HasAnswerText,
    HasProgressValue,
    Protocol,
):
    """Presentation exercise task DTO interface."""
