"""Exercise domain result formatters."""

from typing import TypeVar, override

from contracts.entity.domain.exercise.fields import ExerciseCaseProtocol
from contracts.enums import ExerciseStatus
from contracts.schemas.domain.exercise.flow import (
    ExerciseCase,
    PresentationTask,
    TestExerciseTask,
)
from interfaces.protocols.domain.exercise import (
    PresentationDomainResultProtocol,
    PresentationTaskProtocol,
    TestDomainResultProtocol,
    TestTaskProtocol,
)
from interfaces.schemas.web.task import Option

from .abstract import AbstractConfFormatter

DataT = TypeVar('DataT')
ConfigurationT = TypeVar('ConfigurationT')
DtoT = TypeVar('DtoT')


class PresentationFormatter(
    AbstractConfFormatter[
        PresentationDomainResultProtocol,
        ConfigurationT,
        ExerciseCaseProtocol[PresentationTaskProtocol],
    ],
):
    """Presentation exercise domain result formatter."""

    @override
    def format(
        self,
        data: PresentationDomainResultProtocol,
        conf: ConfigurationT,
    ) -> ExerciseCaseProtocol[PresentationTaskProtocol]:
        """Build a presentation DTO according to the configuration."""
        task = data.item
        return ExerciseCase(
            status=ExerciseStatus.NEW_TASK,
            domain=PresentationTask(
                question_text=task.define,
                answer_text=task.mean,
                progress_value=task.progress_value,
            ),
        )


class TestFormatter(
    AbstractConfFormatter[
        TestDomainResultProtocol,
        ConfigurationT,
        ExerciseCaseProtocol[TestTaskProtocol],
    ],
):
    """Test exercise domain result formatter."""

    __test__ = False

    @override
    def format(
        self,
        data: TestDomainResultProtocol,
        conf: ConfigurationT,
    ) -> ExerciseCaseProtocol[TestTaskProtocol]:
        """Build a test DTO according to the configuration."""
        return ExerciseCase(
            status=ExerciseStatus.NEW_TASK,
            domain=TestExerciseTask(
                question_option_value=data.question_option_value,
                question_text=self._get_question_text(data, conf),
                items=self._get_options(data, conf),
            ),
        )

    def _get_options(
        self,
        data: TestDomainResultProtocol,
        conf: ConfigurationT,
    ) -> list[Option]:
        return [  # type: ignore
            Option(value=value, text=option.mean)
            for value, option in enumerate(data.items)  # type: ignore
        ]

    # FIXME: Fix type hint ignore
    def _get_question_text(
        self,
        data: TestDomainResultProtocol,
        conf: ConfigurationT,
    ) -> str:
        question_option_value = data.question_option_value
        question_option = data.items[question_option_value]  # type: ignore
        return question_option.define  # type: ignore
