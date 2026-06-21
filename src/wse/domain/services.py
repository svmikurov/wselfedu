"""Domain layer services."""

from __future__ import annotations

import logging
from random import randrange, sample
from typing import TYPE_CHECKING

from .values import CheckingResult, Option, Testing

if TYPE_CHECKING:
    from .protocols import (
        CheckableOption,
        HasIsCorrect,
        Testable,
        TestingCreatableSpec,
    )

log = logging.getLogger(__name__)


class CreateTestingService:
    """Domain service for testing creation."""

    def create(
        self,
        spec: TestingCreatableSpec,
    ) -> Testable:
        """Create a testing task from the given candidates."""
        option_count = spec.params.option_count
        learnables = spec.learnables

        selected_index = randrange(option_count)
        user_value = selected_index + 1

        studied_items = sample(learnables, option_count)
        question_item = studied_items[selected_index]

        task = Testing(
            question_text=question_item.define,
            question_value=user_value,
            options=tuple(
                Option(option_value=value, option_text=item.explain)
                for value, item in enumerate(studied_items, start=1)
            ),
        )

        return task


class CheckTestingService:
    """Domain service for testing answer check."""

    def check(self, spec: CheckableOption) -> HasIsCorrect:
        """Check a testing task user answer."""
        return CheckingResult(
            is_correct=spec.answer_value == spec.question_value
        )
