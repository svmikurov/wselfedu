"""Exercise task DTO builder."""

from contracts.entity.domain.exercise import flow
from contracts.schemas.domain.exercise import dtos

from ..aliases import SpecT
from ..protocol import SpecDtoBuilderProtocol


class ExercisePresentationBuilder(
    SpecDtoBuilderProtocol[
        flow.PresentationCaseProtocol,
        SpecT,
        flow.PresentationTaskProtocol,
    ],
):
    """Exercise case DTO null builder."""

    def build(
        self,
        data: flow.PresentationCaseProtocol,
        spec: SpecT,
    ) -> flow.PresentationTaskProtocol:
        """Build presentation exercise task DTO."""
        option = data.domain.option
        return dtos.PresentationTask(
            status=data.status,
            question_text=option.define,
            answer_text=option.mean,
            progress_value=option.progress,
        )


class TestExerciseTaskBuilder(
    SpecDtoBuilderProtocol[
        flow.TestCaseProtocol,
        SpecT,
        flow.TestTaskProtocol,
    ],
):
    """Test exercise task DTO builder."""

    def build(
        self,
        data: flow.TestCaseProtocol,
        spec: SpecT,
    ) -> flow.TestTaskProtocol:
        """Build test exercise task DTO."""
        return dtos.TestExerciseTask(
            status=data.status,
            option_value=data.domain.option_value,
            options=data.domain.options,
        )
