"""Protocol for test exercise interface."""

from typing import Protocol

from interfaces.protocols.domain.exercise import (
    Candidate,
    HasExerciseStatus,
    HasQuestionText,
)

from ..protocol import (
    HasCase,
    HasOptions,
    HasOptionValue,
)


class TestExerciseCaseProtocol(
    HasOptionValue,
    HasOptions[Candidate],
    Protocol,
):
    """Protocol for test exercise case DTO interface."""


class TestExerciseDomainResultProtocol(
    HasExerciseStatus,
    HasCase[TestExerciseCaseProtocol],
    Protocol,
):
    """Protocol for test exercise domain result DTO interface."""


class TestExerciseTaskProtocol(
    HasExerciseStatus,
    HasQuestionText,
    HasOptions[Candidate],
    Protocol,
):
    """Protocol for test exercise task DTO interface."""
