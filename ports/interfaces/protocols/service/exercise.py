"""Protocols for exercise service interface."""

from typing import Protocol, TypeVar

from ports.contract.entity.domain.exercise.fields import (
    HasDomain,
    HasExerciseStatus,
    HasTask,
)
from ports.interfaces.protocols.domain.exercise import (
    PresentationDomainResultProtocol,
    PresentationTaskProtocol,
    TestDomainResultProtocol,
    TestTaskProtocol,
)

DomainT = TypeVar('DomainT')
TaskT = TypeVar('TaskT')


class ExerciseCaseProtocol(
    HasExerciseStatus,
    HasDomain[DomainT],
    HasTask[TaskT],
    Protocol,
):
    """Protocol for exercise case DTO interface."""


class PresentationCaseProtocol(
    ExerciseCaseProtocol[
        PresentationDomainResultProtocol,
        PresentationTaskProtocol,
    ],
    Protocol,
):
    """Protocol for presentation exercise case DTO."""


class TestCaseProtocol(
    ExerciseCaseProtocol[
        TestDomainResultProtocol,
        TestTaskProtocol,
    ],
    Protocol,
):
    """Protocol for test exercise case DTO."""
