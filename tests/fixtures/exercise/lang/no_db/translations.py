"""Language discipline translations."""

from typing import Final

from ports.contract.enums import ExerciseStatus
from ports.interfaces.schemas.domain.exercise.exercise import (
    TaskItem,
    TestTaskDomainResult,
)

TRANSLATIONS: Final[tuple[tuple[str, str], ...]] = (
    ('помидор', 'tomato'),
    ('огурец', 'cucumber'),
    ('яблоко', 'apple'),
    ('белый', 'white'),
    ('черный', 'black'),
    ('красный', 'red'),
    ('зеленый', 'green'),
    ('оранжевый', 'orange'),
    # QUESTION: Add ('апельсин', 'orange')?
    # ('апельсин', 'orange'),
)

TRANSLATION_INDEX = 3
"""Selected translations fixture index for task question.
"""

TASK_ITEMS = [
    TaskItem(
        pk=pk,
        define=define,
        mean=mean,
        progress_value=0,
    )
    for pk, (define, mean) in enumerate(TRANSLATIONS, start=1)
]

TEST_TASK_DOMAIN_RESULT = TestTaskDomainResult(
    question_option_value=TRANSLATION_INDEX,
    items=TASK_ITEMS,
    status=ExerciseStatus.NEW_TASK,
)
