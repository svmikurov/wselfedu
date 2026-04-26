"""Exercise case DTO builder."""

from typing import TypeVar

from interfaces.entity.domain.exercise import fields, flow
from interfaces.schemas.domain.exercise import dtos

from ..protocol import ExerciseTaskBuilderProtocol

SpecT = TypeVar('SpecT')


class ExercisePresentationBuilder(
    ExerciseTaskBuilderProtocol[
        flow.PresentationDomainResultProtocol,
        SpecT,
        flow.PresentationCaseProtocol,
    ],
):
    """Exercise case DTO null builder."""

    def build(
        self,
        case: flow.PresentationDomainResultProtocol,
        spec: SpecT,
    ) -> flow.PresentationCaseProtocol:
        """Build exercise case DTO."""
        return dtos.PresentationExerciseCase(
            status=case.status,
            domain=case,
        )


class TestExerciseTaskBuilder(
    ExerciseTaskBuilderProtocol[
        flow.TestDomainResultProtocol,
        SpecT,
        flow.TestCaseProtocol,
    ],
):
    """Test exercise task DTO builder."""

    def build(
        self,
        case: flow.TestDomainResultProtocol,
        spec: SpecT,
    ) -> flow.TestCaseProtocol:
        """Build exercise case DTO."""
        return dtos.TestExerciseCase(
            status=case.status,
            domain=case,
        )
