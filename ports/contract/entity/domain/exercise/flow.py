"""Protocols for exercise DTO interface flow."""

from typing import Protocol, TypeVar

from ports.contract import enums
from ports.contract.entity.domain.exercise import fields as exercise
from ports.contract.entity.general import HasStatus
from ports.interfaces.protocols.domain.exercise import (
    CandidateProtocol,
    CandidatesT,
)

DomainResultT = TypeVar('DomainResultT', bound='ExerciseDomainResultProtocol')


# =================================================
# Exercise domain result
# =================================================


class ExerciseDomainResultProtocol(
    exercise.HasExerciseStatus,
    Protocol,
):
    """Protocol for exercise domain result DTO."""


class PresentationDomainResultProtocol(
    ExerciseDomainResultProtocol,
    exercise.HasTaskItem[CandidateProtocol],
    Protocol,
):
    """Protocol for presentation exercise domain result DTO."""


class TestDomainResultProtocol(
    ExerciseDomainResultProtocol,
    exercise.HasQuestionOptionValue,
    exercise.HasTaskItems[CandidatesT],
    Protocol,
):
    """Protocol for test exercise domain result DTO."""


# =================================================
# Exercise case
# =================================================


class ExerciseCaseProtocol(
    HasStatus[enums.ExerciseStatus],
    exercise.HasDomain[DomainResultT],
    Protocol[DomainResultT],
):
    """Protocol for exercise case DTO."""


class PresentationCaseProtocol(
    ExerciseCaseProtocol[PresentationDomainResultProtocol],
    Protocol,
):
    """Protocol for presentation exercise case DTO."""


class TestCaseProtocol(
    ExerciseCaseProtocol[TestDomainResultProtocol],
    Protocol,
):
    """Protocol for presentation exercise case DTO."""
