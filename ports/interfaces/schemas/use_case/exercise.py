"""Exercise use case result DTO schema."""

from typing import Generic, TypeVar

from ports.contract.enums import ExerciseStatus
from ports.interfaces.schemas.fields import StatusField, TaskField

T = TypeVar('T')


class ExerciseUseCaseResult(
    StatusField[ExerciseStatus],
    TaskField[T],
    Generic[T],
):
    """Exercise use case result schema."""
