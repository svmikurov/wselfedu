"""Exercise case DTO builder."""

from typing import TypeVar

from ports.abstract.builder import AbstractSpecDtoBuilder
from ports.contract.entity.domain.exercise.fields import HasExerciseStatus
from ports.contract.entity.domain.exercise.flow import ExerciseCaseProtocol
from ports.interfaces.schemas.domain.exercise.flow import ExerciseCase

CaseT = TypeVar('CaseT')
SpecT = TypeVar('SpecT')
DomainT = TypeVar('DomainT', bound=HasExerciseStatus)


class ExerciseCaseBuilder(
    AbstractSpecDtoBuilder[
        DomainT,
        SpecT,
        ExerciseCaseProtocol[HasExerciseStatus],
    ],
):
    """Exercise case DTO null builder."""

    def build(
        self,
        data: DomainT,
        spec: SpecT,
    ) -> ExerciseCaseProtocol[HasExerciseStatus]:
        """Build exercise case DTO."""
        return ExerciseCase(
            status=data.status,
            domain=data,
        )
