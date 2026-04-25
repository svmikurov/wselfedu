"""General interface."""

from typing import Protocol, TypeVar

T = TypeVar('T')


class NullProtocol(Protocol):
    """Null interface."""


class HasResourceIdentifier(Protocol):
    """Protocol for has resource identifier interface."""

    pk: int


class HasText(Protocol):
    """Protocol for has *text* interface."""

    text: str


class HasContext(Protocol[T]):
    """Protocol for has *context* interface."""

    context: T


class PersonProtocol(Protocol):
    """Protocol for user interface."""
