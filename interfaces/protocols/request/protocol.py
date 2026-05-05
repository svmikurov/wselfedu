"""Protocol for request interface."""

from typing import Protocol


class HasIsHtmx(Protocol):
    """Protocol for has *is_htmx* interface."""

    is_htmx: bool
