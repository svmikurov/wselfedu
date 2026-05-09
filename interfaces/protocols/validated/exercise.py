"""Exercise perform request data interfaces."""

from typing import Protocol

from contracts.entity.domain.exercise.fields import HasOptionValue
from contracts.entity.domain.general import HasAction
from contracts.enums import ExerciseAction


class ValidatedCreateTaskRequestProtocol(
    HasAction[ExerciseAction],
    Protocol,
):
    """Protocol for *create task* request data interface.

    Parameters
    ----------
    action : `ExerciseAction`
        Exercise performing action (e.g., 'create task', 'check answer')

    """


class ValidatedCheckTestRequestProtocol(
    HasAction[ExerciseAction],
    HasOptionValue,
    Protocol,
):
    """Protocol for *check test answer* request data interface.

    Parameters
    ----------
    action : `ExerciseAction`
        Exercise performing action (e.g., 'create task', 'check answer')
    option_value : `int`
        User answer test task option value.

    """
