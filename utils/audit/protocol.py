"""Protocol for audit interface."""

from typing import Protocol


class AuditorProtocol(Protocol):
    """Protocol for audit record interface."""

    def record(self, step_name: str, **kwargs: object) -> None:
        """Record attributes."""
