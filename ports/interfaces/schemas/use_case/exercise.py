"""Exercise use case result DTO schema."""

from typing import Generic, TypeVar

from ports.contract.enums import ExerciseStatus
from ports.interfaces.schemas.domain.exercise import (
    PresentationTaskDomainResult,
    TestTaskDomainResult,
)
from ports.interfaces.schemas.fields import StatusField, TaskField

T = TypeVar('T')


class ExerciseUseCaseResult(
    StatusField[ExerciseStatus],
    TaskField[T],
    Generic[T],
):
    """Exercise use case result schema."""


TestUseCaseResult = ExerciseUseCaseResult[TestTaskDomainResult]
"""Test exercise use case result schema.
"""

PresentationUseCaseResult = ExerciseUseCaseResult[PresentationTaskDomainResult]
"""Presentation exercise use case result schema.
"""
