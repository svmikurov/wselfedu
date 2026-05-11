"""Exercise task DTO builder."""

from typing import TypeVar

from ports.contract.infra.builder import SpecDtoBuilderProtocol
from ports.interfaces.protocols.domain import exercise as interfaces
from ports.interfaces.protocols.service.exercise import (
    PresentationCaseProtocol,
    TestCaseProtocol,
)
from ports.interfaces.schemas.domain.exercise.flow import (
    PresentationTask,
    TestTask,
)
from ports.interfaces.schemas.web.task import Option
from utils.audit.base import BaseAuditable

SpecT = TypeVar('SpecT')


class ExercisePresentationBuilder(
    BaseAuditable,
    SpecDtoBuilderProtocol[
        PresentationCaseProtocol,
        SpecT,
        interfaces.PresentationTaskProtocol,
    ],
):
    """Presentation exercise task DTO builder."""

    def build(
        self,
        data: PresentationCaseProtocol,
        spec: SpecT,
    ) -> interfaces.PresentationTaskProtocol:
        """Build presentation exercise task DTO."""
        option = data.domain.item
        return PresentationTask(
            question_text=option.define,
            answer_text=option.mean,
            progress_value=option.progress_value,
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
        return TestTask(
            question_option_value=data.domain.question_option_value,
            question_text='',
            items=[
                Option(value=value, text=option.mean)
                for value, option in enumerate(data.domain.items)
            ],
        )
