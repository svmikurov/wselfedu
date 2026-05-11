"""Exercise domain result formatters."""

from typing import TypeVar, override

from ports.abstract.formatter import AbstractConfFormatter
from ports.contract.entity.domain.exercise import HasDisplayOrder
from ports.contract.enums import DisplayOrder, ExerciseStatus
from ports.interfaces.protocols.domain.exercise import (
    PresentationDomainResultProtocol,
    TestDomainResultProtocol,
)
from ports.interfaces.protocols.service.exercise import (
    PresentationCaseProtocol,
    TestCaseProtocol,
)
from ports.interfaces.schemas.domain.exercise.flow import (
    ExerciseCase,
    PresentationTask,
    TestTask,
)
from ports.interfaces.schemas.web.task import Option

DataT = TypeVar('DataT')
ConfigurationT = TypeVar('ConfigurationT', bound=HasDisplayOrder[DisplayOrder])
DtoT = TypeVar('DtoT')

QUESTION_INDEX = 0
ANSWER_INDEX = 1


class PresentationFormatter(
    AbstractConfFormatter[
        PresentationDomainResultProtocol,
        ConfigurationT,
        PresentationCaseProtocol,
    ],
):
    """Presentation exercise domain result formatter."""

    @override
    def format(
        self,
        data: PresentationDomainResultProtocol,
        conf: ConfigurationT,
    ) -> PresentationCaseProtocol:
        """Build a presentation DTO according to the configuration."""
        task = data.item
        return ExerciseCase(
            status=ExerciseStatus.NEW_TASK,
            domain=data,
            task=PresentationTask(
                question_text=task.define,
                answer_text=task.mean,
                progress_value=task.progress_value,
            ),
        )


class TestFormatter(
    AbstractConfFormatter[
        TestDomainResultProtocol,
        ConfigurationT,
        TestCaseProtocol,
    ],
):
    """Test exercise domain result formatter."""

    __test__ = False

    @override
    def format(
        self,
        data: TestDomainResultProtocol,
        conf: ConfigurationT,
    ) -> TestCaseProtocol:
        """Build a test DTO according to the configuration."""
        return ExerciseCase(
            status=ExerciseStatus.NEW_TASK,
            domain=data,
            task=TestTask(  # type: ignore
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
        return [
            Option(value=value, text=self._get_answer(option, conf))  # type: ignore
            for value, option in enumerate(data.items)
        ]

    # FIXME: Fix type hint ignore
    def _get_question_text(
        self,
        data: TestDomainResultProtocol,
        conf: ConfigurationT,
    ) -> str:
        question_option_value = data.question_option_value
        question_option = data.items[question_option_value]
        return self._get_question(question_option, conf)  # type: ignore

    def _get_question(
        self, item: TestDomainResultProtocol, conf: ConfigurationT
    ) -> str:
        """Return option question text."""
        orders = DisplayOrder.get_display_phases(conf.display_order)
        return str(getattr(item, orders[QUESTION_INDEX]))

    def _get_answer(
        self, item: TestDomainResultProtocol, conf: ConfigurationT
    ) -> str:
        """Return option answer text."""
        orders = DisplayOrder.get_display_phases(conf.display_order)
        return str(getattr(item, orders[ANSWER_INDEX]))
