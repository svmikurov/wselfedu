"""Response's general interface."""

from typing import Protocol


class NullContextProtocol(Protocol):
    """Null context DTO."""

    __slots__ = ()


class HasOob(Protocol):
    """Protocol for has Out Of Bound interface."""

    oob_html: str
