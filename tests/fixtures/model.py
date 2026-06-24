"""Domain model fixtures."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from wse.config import DATA_PATH
from wse.domain.entities import StudyItem
from wse.domain.values import Option, Testing
from wse.utils.io import load_json

if TYPE_CHECKING:
    from tests.types import LearnableTypedData
    from wse.domain.protocols import Testable, UniqueLearnable

# Testing exercise test configuration
TASK_SESSION_ID: str = 'test_session_123'
TESTING_TASK_OPTION_COUNT: int = 3
CORRECT_ANSWER_LEARNABLE_INDEX: int = 0
CORRECT_ANSWER_OPTION_VALUE: int = 1
INCORRECT_ANSWER_OPTION_VALUE: int = 2


@pytest.fixture
def testing_task(learnables: tuple[UniqueLearnable, ...]) -> Testable:
    """Provide a testing exercise task."""
    return Testing(
        question_text=learnables[CORRECT_ANSWER_LEARNABLE_INDEX].define,
        question_value=CORRECT_ANSWER_OPTION_VALUE,
        options=tuple(
            Option(option_value=value, option_text=item.explain)
            for value, item in enumerate(
                learnables[:TESTING_TASK_OPTION_COUNT], start=1
            )
        ),
    )


@pytest.fixture
def learnables() -> tuple[UniqueLearnable, ...]:
    """Provide exercise task candidates."""
    items: list[LearnableTypedData] = load_json(DATA_PATH / 'candidates.json')
    return tuple(StudyItem(**data) for data in items)
