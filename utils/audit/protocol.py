"""Protocol for audit interface."""

from typing import Protocol


class Auditable(Protocol):
    """Protocol for auditable interface."""

    @property
    def name(self) -> str:
        """Provide name of auditable object."""


class AuditorProtocol(Protocol):
    """Protocol for audit record interface."""

    def record(
        self,
        step_name: str,
        obj: Auditable | None = None,
        **kwargs: object,
    ) -> None:
        """Record attributes."""
