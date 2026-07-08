"""Domain layer enumeration."""

from enum import Enum


class ExerciseAction(Enum):
    """Exercise action enumeration."""

    CREATE_TASK = 'create_task'
    CHECK_ANSWER = 'check_answer'
