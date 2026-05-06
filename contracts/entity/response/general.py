"""Response's general interface."""

from typing import Protocol


class NullContextProtocol(Protocol):
    """Null context DTO."""

    __slots__ = ()


class HasHtml(Protocol):
    """Protocol for has HTML interface."""

    html: str
