"""Protocol for exercise use case result interface."""

from typing import Protocol, TypeVar

from ports.contract.entity.domain.exercise import HasExerciseStatus, HasTask
from ports.interfaces.protocols.domain.exercise import TestTaskProtocol

T_co = TypeVar('T_co', covariant=True)


class ExerciseUseCaseResultProtocol(
    HasExerciseStatus,
    HasTask[T_co],
    Protocol,
):
    """Protocol for exercise use case result interface."""


TestUseCaseResultProtocol = ExerciseUseCaseResultProtocol[TestTaskProtocol]
