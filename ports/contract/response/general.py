"""Response's general interface."""

from typing import Protocol


class HasHtml(Protocol):
    """Protocol for has HTML interface."""

    html: str
