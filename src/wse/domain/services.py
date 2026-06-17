"""Domain layer services."""

from __future__ import annotations

from random import randrange, sample
from typing import TYPE_CHECKING

from .values import CheckingResult, Option, Testing

if TYPE_CHECKING:
    from .protocols import (
        CheckableOption,
        HasIsCorrect,
        HasLearnables,
        Testable,
        UniqueLearnable,
    )


def create_testing_task(
    spec: HasLearnables[list[UniqueLearnable]],
) -> Testable:
    """Create a testing task from the given candidates."""
    options_count = 3

    selected_index = randrange(options_count)
    user_value = selected_index + 1

    studied_items = sample(spec.learnables, options_count)
    question_item = studied_items[selected_index]

    task = Testing(
        question_text=question_item.define,
        question_value=user_value,
        options=[
            Option(option_value=value, option_text=item.explain)
            for value, item in enumerate(studied_items, start=1)
        ],
    )

    return task


def check_testing_answer(spec: CheckableOption) -> HasIsCorrect:
    """Check a testing task user answer."""
    return CheckingResult(is_correct=spec.answer_value == spec.question_value)
