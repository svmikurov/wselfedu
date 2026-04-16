"""General interface."""

from typing import Protocol


class NullProtocol(Protocol):
    """Nul interface."""


class HasText(Protocol):
    """Protocol for has *text* interface."""

    text: str
