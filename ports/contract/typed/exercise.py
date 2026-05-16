"""Typed exercise data."""

from typing import Generic, Literal, TypedDict, TypeVar

T = TypeVar('T')


class TypedExerciseAction(TypedDict, Generic[T]):
    """Typed exercise action string representation."""

    action: T


class TypedOptionValue(TypedDict):
    """Typed *option_value* string representation."""

    option_value: str


class TypedIsKnown(TypedDict):
    """Typed *is_known* boolean value string representation."""

    is_known: Literal['true', 'false']
