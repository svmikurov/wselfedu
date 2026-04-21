"""General interface."""

from typing import Protocol


class NullProtocol(Protocol):
    """Nul interface."""


class HasResourceIdentifier(Protocol):
    """Protocol for has resource identifier object interface."""

    pk: int


class HasText(Protocol):
    """Protocol for has *text* interface."""

    text: str
