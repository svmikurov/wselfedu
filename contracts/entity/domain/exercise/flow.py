"""Protocols for exercise DTO interface flow."""

from typing import Protocol, TypeVar

from contracts import enums
from contracts.entity.domain.exercise import fields as exercise
from contracts.entity.general import HasStatus

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
    exercise.HasExerciseDomainOption,
    Protocol,
):
    """Protocol for presentation exercise domain result DTO."""


class TestDomainResultProtocol(
    ExerciseDomainResultProtocol,
    exercise.HasQuestionOptionValue,
    exercise.HasExerciseDomainOptions,
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


# =================================================
# Exercise task
# =================================================


class TaskProtocol(
    exercise.HasExerciseStatus,
    Protocol,
):
    """Protocol for exercise task DTO."""


class PresentationTaskProtocol(
    TaskProtocol,
    exercise.HasQuestionText,
    exercise.HasAnswerText,
    exercise.HasProgressValue,
    Protocol,
):
    """Protocol for presentation exercise task DTO."""


class TestTaskProtocol(
    TaskProtocol,
    exercise.HasQuestionOptionValue,
    exercise.HasExerciseDomainOptions,
    Protocol,
):
    """Protocol for test exercise task DTO."""
