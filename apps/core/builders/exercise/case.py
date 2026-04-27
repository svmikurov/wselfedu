"""Exercise case DTO builder."""

from typing import TypeVar

from interfaces.entity.domain.exercise import fields, flow
from interfaces.schemas.domain.exercise import dtos

from ..protocol import SpecDtoBuilderProtocol

CaseT = TypeVar('CaseT')
SpecT = TypeVar('SpecT')
DomainT = TypeVar('DomainT', bound=fields.HasExerciseStatus)


class ExerciseCaseBuilder(
    SpecDtoBuilderProtocol[
        DomainT,
        SpecT,
        flow.ExerciseCaseProtocol[fields.HasExerciseStatus],
    ],
):
    """Exercise case DTO null builder."""

    def build(
        self,
        data: DomainT,
        spec: SpecT,
    ) -> flow.ExerciseCaseProtocol[fields.HasExerciseStatus]:
        """Build exercise case DTO."""
        return dtos.ExerciseCase(
            status=data.status,
            domain=data,
        )
