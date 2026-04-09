"""Exercise enumerations."""

from __future__ import annotations

from random import shuffle

from apps.core.enums import BaseEnum

DEFINITION_INDEX = 0
EXPLANATION_INDEX = 1


class ExerciseTypeEnum(BaseEnum):
    """Exercise type enumeration."""

    TEST = 'test'
    PRESENTATION = 'presentation'


class ExerciseProcessEnum(BaseEnum):
    """Exercise process request enumeration."""

    CREATE_CASE = 'create_case'
    CHECK_ANSWER = 'check_answer'
    UPDATE_PROGRESS = 'update_progress'
    UPDATE_FAVORITES = 'update_favorites'
    EXPLAIN_CASE = 'explain_case'
    EXPLAIN_OPTION = 'explain_option'


class ExerciseStatusEnum(BaseEnum):
    """Exercise status (domain result) enumeration."""

    NEW_TASK = 'new_task'
    ANSWER = 'user_answer'
    CORRECT = 'correct_answer'
    WRONG = 'wrong_answer'
    EXPLAIN = 'correct and wrong answer explanation'
    NO_CASE = 'no_available_cases'
    UPDATED_PROGRESS = 'updated progress'


class DisplayOrder(BaseEnum):
    """Exercise items display order.

    An enumeration instance defines order as order from instance value.

    Enumerations:
        - From definition to meaning
        - From meaning to definition
        - Random order
    """

    DEFINE = 'define'  # Item definition
    MEAN = 'mean'  # Item meaning
    RANDOM = 'random'

    def get_display_phases(self) -> list[DisplayOrder]:
        """Get translation order."""
        order = [self.DEFINE, self.MEAN]
        match self:
            case self.DEFINE:
                pass
            case self.MEAN:
                order.reverse()
            case self.RANDOM:
                shuffle(order)
        return order
