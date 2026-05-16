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
type TestActionDataU = Union[
    TypedCreateTask,
    TypedCheckTest,
]
type ExerciseActionU = Union[
    PresentationActionDataU,
    TestActionDataU,
]
