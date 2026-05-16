"""Typed exercise data."""

from typing import Generic, Literal, TypedDict, TypeVar

T = TypeVar('T')


class TypedAction(TypedDict, Generic[T]):
    """Typed action representation."""

    action: T


class TypedOptionValue(TypedDict):
    """Typed *option_value* string representation."""

    option_value: str


class TypedIsKnown(TypedDict):
    """Typed *is_known* boolean literal representation."""

    is_known: Literal['true', 'false']
