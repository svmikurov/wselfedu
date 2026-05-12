"""Protocol for exercise use case result interface."""

from typing import Protocol, TypeVar

from ports.contract.entity.domain.exercise import HasExerciseStatus, HasTask
from ports.interfaces.protocols.domain import (
    PresentationTaskProtocol,
    TestTaskProtocol,
)

T_co = TypeVar('T_co', covariant=True)


class ExerciseUseCaseResultProtocol(
    HasExerciseStatus,
    HasTask[T_co],
    Protocol,
):
    """Protocol for exercise use case result interface.

    Parameters
    ----------
    status : `ExerciseStatus`
        Exercise status.
    task : `T`
        Exercise task (e.g., presentation, task).

    """


PresentationUseCaseResultProtocol = ExerciseUseCaseResultProtocol[
    PresentationTaskProtocol,
]
"""Protocol for *presentation* exercise use case result interface.
"""

TestUseCaseResultProtocol = ExerciseUseCaseResultProtocol[TestTaskProtocol]
"""Protocol for *test* exercise use case result interface.
"""
