"""Exercise task DTO builder."""

from contracts.entity.domain.exercise.flow import (
    PresentationCaseProtocol,
    TestCaseProtocol,
)
from contracts.schemas.domain.exercise.flow import (
    PresentationTask,
    TestExerciseTask,
)
from interfaces.protocols.domain import exercise as interfaces
from interfaces.schemas.domain.exercise import Option
from utils.audit.base import BaseAuditable

from ..aliases import SpecT
from ..protocol import SpecDtoBuilderProtocol


class ExercisePresentationBuilder(
    BaseAuditable,
    SpecDtoBuilderProtocol[
        PresentationCaseProtocol,
        SpecT,
        interfaces.PresentationTaskProtocol,
    ],
):
    """Exercise case DTO null builder."""

    def build(
        self,
        data: PresentationCaseProtocol,
        spec: SpecT,
    ) -> interfaces.PresentationTaskProtocol:
        """Build presentation exercise task DTO."""
        option = data.domain.option
        return PresentationTask(
            status=data.status,
            question_text=option.define,
            answer_text=option.mean,
            progress_value=option.progress,
        )


class TestExerciseTaskBuilder(
    BaseAuditable,
    SpecDtoBuilderProtocol[
        TestCaseProtocol,
        SpecT,
        interfaces.TestTaskProtocol,
    ],
):
    """Test exercise task DTO builder."""

    def build(
        self,
        data: TestCaseProtocol,
        spec: SpecT,
    ) -> interfaces.TestTaskProtocol:
        """Build test exercise task DTO."""
        return TestExerciseTask(
            status=data.status,
            question_option_value=data.domain.question_option_value,
            options=[  # type: ignore
                Option(value=value, text=option.mean)
                for value, option in enumerate(data.domain.options)
            ],
        )
