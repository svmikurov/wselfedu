"""Exercise use case result builder."""

from typing import Protocol, TypeVar

from ports.abstract.builder import AbstractSpecDtoBuilder
from ports.contract.entity.domain.exercise import HasExerciseStatus, HasTask
from ports.interfaces.protocols.use_case.exercise import (
    ExerciseUseCaseResultProtocol,
)
from ports.interfaces.schemas.use_case.exercise import ExerciseUseCaseResult

Task_co = TypeVar('Task_co', covariant=True)
TaskT = TypeVar('TaskT')
SpecT = TypeVar('SpecT')


class _CaseProtocol(
    HasExerciseStatus,
    HasTask[Task_co],
    Protocol,
):
    """Protocol for case interface."""


class ExerciseUseCaseResultBuilder(
    AbstractSpecDtoBuilder[
        _CaseProtocol[TaskT], SpecT, ExerciseUseCaseResultProtocol[TaskT]
    ],
):
    """Exercise use case result DTO builder."""

    def build(
        self,
        case: _CaseProtocol[TaskT],
        spec: SpecT,
    ) -> ExerciseUseCaseResultProtocol[TaskT]:
        """Build exercise use case result DTO."""
        return ExerciseUseCaseResult(
            status=case.status,
            task=case.task,
        )
