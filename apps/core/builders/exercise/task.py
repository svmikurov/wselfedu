"""Exercise task DTO builder."""

from typing import TypeVar

from interfaces.entity.domain.exercise import fields, flow
from interfaces.schemas.domain.exercise import dtos
from interfaces.schemas.domain.exercise.task import PresentationTask

from ..protocol import ExerciseTaskBuilderProtocol

SpecT = TypeVar('SpecT')


class ExercisePresentationBuilder(
    ExerciseTaskBuilderProtocol[
        flow.PresentationCaseProtocol,
        SpecT,
        flow.PresentationTaskProtocol,
    ],
):
    """Exercise case DTO null builder."""

    def build(
        self,
        case: flow.PresentationCaseProtocol,
        spec: SpecT,
    ) -> flow.PresentationTaskProtocol:
        """Build presentation exercise task DTO."""
        option = case.domain.option
        return PresentationTask(
            status=case.status,
            question_text=option.define,
            answer_text=option.mean,
            progress_value=option.progress,
        )


class TestExerciseTaskBuilder(
    ExerciseTaskBuilderProtocol[
        flow.TestCaseProtocol,
        SpecT,
        flow.TestTaskProtocol,
    ],
):
    """Test exercise task DTO builder."""

    def build(
        self,
        case: flow.TestCaseProtocol,
        spec: SpecT,
    ) -> flow.TestTaskProtocol:
        """Build test exercise task DTO."""
        return dtos.TestTask[fields.Candidates](
            status=case.status,
            option_value=case.domain.option_value,
            options=case.domain.options,
        )
