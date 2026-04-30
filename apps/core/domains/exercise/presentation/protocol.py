"""Protocol for presentation exercise interface."""

from typing import Protocol, TypeVar

from contracts.entity.domain.exercise.fields import (
    Candidate,
    HasAnswerText,
    HasExerciseDomainOption,
    HasExerciseStatus,
    HasProgressValue,
    HasQuestionOptionValue,
    HasQuestionText,
)

from ..protocol import (
    HasCase,
)

OptionT = TypeVar('OptionT', bound=Candidate)


# DEPRECATED: Remove `PresentationCreateResultProtocol`
class PresentationCreateResultProtocol(
    HasExerciseDomainOption,
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
    HasQuestionOptionValue,
    HasExerciseDomainOption,
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
