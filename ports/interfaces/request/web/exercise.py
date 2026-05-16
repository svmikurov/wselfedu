"""Typed WEB exercise request data."""

from typing import Literal, Union

from ports.contract.enums import ExerciseAction
from ports.contract.typed.exercise import (
    TypedExerciseAction,
    TypedIsKnown,
    TypedOptionValue,
)


class CreateTaskRequestData(
    TypedExerciseAction[Literal[ExerciseAction.CREATE_TASK]]
):
    """Typed create task request data.

    Parameters
    ----------
    action : `Literal['create_task']`
        Exercise action enumeration.

    """


class CheckTestRequestData(
    TypedExerciseAction[Literal[ExerciseAction.CHECK_ANSWER]],
    TypedOptionValue,
):
    """Typed user test answer request data.

    Parameters
    ----------
    action : `Literal['check_answer']`
        Exercise action enumeration.
    option_value : `str`
        User answer test option value.

    """


class UpdateProgressRequestData(
    TypedExerciseAction[Literal[ExerciseAction.UPDATE_PROGRESS]],
    TypedIsKnown,
):
    """Typed item study progress update data.

    Parameters
    ----------
    action : `Literal['update_progress']`
        Exercise action enumeration.
    is_known : `Literal['true', 'false']`
        Boolean flag for progress action.

    """


# =================================================
# Union typed data
# =================================================


type PresentationActionDataU = Union[
    CreateTaskRequestData,
    UpdateProgressRequestData,
]

type TestActionDataU = Union[
    CreateTaskRequestData,
    CheckTestRequestData,
]

type ExerciseActionU = Union[
    PresentationActionDataU,
    TestActionDataU,
]
