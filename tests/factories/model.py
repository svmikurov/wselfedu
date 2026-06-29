"""Domain model factories."""

from __future__ import annotations

from typing import TYPE_CHECKING

from wse.application.dto import Task
from wse.config import DATA_PATH
from wse.domain.entities import StudyItem
from wse.domain.values import Option, Testing
from wse.utils.io import load_json

if TYPE_CHECKING:
    from tests.test_types import LearnableTypedData
    from wse.application.protocols import TaskDtoProto
    from wse.domain.protocols import Testable, UniqueLearnable

# Testing exercise test configuration
TASK_SESSION_ID: str = 'test_session_123'
TESTING_TASK_OPTION_COUNT: int = 3
CORRECT_ANSWER_LEARNABLE_INDEX: int = 0
CORRECT_ANSWER_OPTION_VALUE: int = 1
INCORRECT_ANSWER_OPTION_VALUE: int = 2


def get_learnables() -> tuple[UniqueLearnable, ...]:
    """Get exercise task candidates to study."""
    items: list[LearnableTypedData] = load_json(DATA_PATH / 'candidates.json')
    return tuple(StudyItem(**data) for data in items)


def create_testing_task(
    learnables: tuple[UniqueLearnable, ...],
    option_count: int = TESTING_TASK_OPTION_COUNT,
    correct_index: int = CORRECT_ANSWER_LEARNABLE_INDEX,
    correct_value: int = CORRECT_ANSWER_OPTION_VALUE,
) -> Testable:
    """Create a testing exercise task."""
    return Testing(
        question_text=learnables[correct_index].define,
        question_value=correct_value,
        options=tuple(
            Option(option_value=value, option_text=item.explain)
            for value, item in enumerate(learnables[:option_count], start=1)
        ),
    )


def create_testing_task_dto(testing_task: Testable) -> TaskDtoProto[Testable]:
    """Provide a testing task DTO."""
    return Task(task=testing_task, session_id=TASK_SESSION_ID)
