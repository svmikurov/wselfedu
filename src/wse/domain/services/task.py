"""Service for exercise tasks."""

from random import choice, randrange, sample
from typing import override

from wse.domain.protocols import (
    CheckableOption,
    HasCorrect,
    Presentable,
    Testable,
    UniqueLearnable,
)
from wse.domain.values import CheckingResult, Option, Presentation, Testing

from .abstract import AbstractCheckAnswerService, AbstractCreateTaskService


class CreatePresentationService(AbstractCreateTaskService[Presentable]):
    """Service for creating presentation tasks."""

    @override
    def execute(self, candidates: list[UniqueLearnable]) -> Presentable:
        """Create a presentation task from a random candidate."""
        studied_item = choice(candidates)
        task = Presentation(
            question_text=studied_item.define,
            answer_text=studied_item.explain,
        )
        return task


class CreateTestingService(AbstractCreateTaskService[Testable]):
    """Service for creating testing tasks with choice options."""

    @override
    def execute(self, candidates: list[UniqueLearnable]) -> Testable:
        """Create a multiple-choice test task with random candidates."""
        options_count = 3

        selected_index = randrange(options_count)
        user_value = selected_index + 1

        studied_items = sample(candidates, options_count)
        studied_item = studied_items[selected_index]

        task = Testing(
            question_text=studied_item.define,
            question_value=user_value,
            options=[
                Option(value=value, text=item.explain)
                for value, item in enumerate(studied_items, start=1)
            ],
        )

        return task  # type: ignore


class CheckTestingService(
    AbstractCheckAnswerService[CheckableOption, HasCorrect],
):
    """Service for checking testing answer with choice options."""

    @override
    def execute(self, spec: CheckableOption) -> HasCorrect:
        return CheckingResult(
            is_correct=spec.question_value == spec.answer_value
        )
