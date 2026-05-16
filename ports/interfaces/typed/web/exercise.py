"""Typed WEB exercise request data."""

from typing import TypedDict, Union

from ports.contract.enums import ExerciseAction


class TypedCreateTask(TypedDict):
    """Typed create task request data."""

    action: ExerciseAction


class TypedCheckTest(TypedDict):
    """Typed user test answer request data."""

    action: ExerciseAction
    option_value: str


type PresentationActionDataU = TypedCreateTask
"""
Parameters
----------
action : `ExerciseAction`
    Exercise action enumeration.
"""

type TestActionDataU = Union[
    TypedCreateTask,
    TypedCheckTest,
]
"""
Parameters
----------
action : `ExerciseAction`
    Exercise action enumeration.
option_value : `str`
    User answer test option value.
"""

type ExerciseActionU = Union[
    PresentationActionDataU,
    TestActionDataU,
]
