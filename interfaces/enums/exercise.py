"""Exercise enumerations."""

from __future__ import annotations

from random import shuffle
from typing import Self

from .base import BaseEnum

DEFINITION_INDEX = 0
EXPLANATION_INDEX = 1


class ExerciseKind(BaseEnum):
    """Exercise kind enumeration."""

    TEST = 'test'
    PRESENTATION = 'presentation'


class ExerciseAction(BaseEnum):
    """Exercise action request enumeration."""

    CREATE_TASK = 'create_task'
    CHECK_ANSWER = 'check_answer'
    UPDATE_PROGRESS = 'update_progress'
    UPDATE_FAVORITES = 'update_favorites'
    EXPLAIN_TASK = 'explain_task'
    EXPLAIN_CASE = 'explain_case'
    EXPLAIN_OPTION = 'explain_option'


class ExerciseStatus(BaseEnum):
    """Exercise status (domain result) enumeration."""

    NEW_TASK = 'new_task'
    ANSWER = 'user_answer'
    CORRECT = 'correct_answer'
    WRONG = 'wrong_answer'
    EXPLAIN = 'correct and wrong answer explanation'
    NO_CASE = 'no_available_cases'
    UPDATED_PROGRESS = 'updated_progress'


class DisplayOrder(BaseEnum):
    """Exercise phase display order.

    Enumerations:
        - DEFINE: From definition to meaning
        - MEAN: From meaning to definition
        - RANDOM: Random order
    """

    DEFINE = 'define'
    MEAN = 'mean'
    RANDOM = 'random'

    def get_display_phases(self) -> list[Self]:
        """Get display order based on current enumeration value.

        Returns:
            list[Self]: Ordered list of display phases.

        """
        phases = [DisplayOrder.DEFINE, DisplayOrder.MEAN]

        match self:
            case DisplayOrder.MEAN:
                phases.reverse()
            case DisplayOrder.RANDOM:
                shuffle(phases)

        return phases
