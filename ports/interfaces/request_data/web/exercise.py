"""Typed WEB exercise request data."""

from typing import Literal, Union

from ports.contract.enums import ExerciseAction
from ports.contract.typed.exercise import (
    TypedAction,
    TypedIsKnown,
    TypedOptionValue,
)


class CreateTaskData(TypedAction[Literal[ExerciseAction.CREATE_TASK]]):
    """Create task request typed data.

    Parameters
    ----------
    action : `Literal['create_task']`
        Exercise action enumeration.

    """


class CheckTestData(
    TypedAction[Literal[ExerciseAction.CHECK_ANSWER]],
    TypedOptionValue,
):
    """User test answer request typed data.

    Parameters
    ----------
    action : `Literal['check_answer']`
        Exercise action enumeration.
    option_value : `str`
        User answer test option value.

    """


class UpdateProgressData(
    TypedAction[Literal[ExerciseAction.UPDATE_PROGRESS]],
    TypedIsKnown,
):
    """Item study progress update typed data.

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


type PresentationDataU = Union[
    CreateTaskData,
    UpdateProgressData,
]

type TestDataU = Union[
    CreateTaskData,
    CheckTestData,
]

type ExerciseDataU = Union[
    PresentationDataU,
    TestDataU,
]
