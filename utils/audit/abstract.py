"""Abstract base class for auditor."""

from abc import ABC, abstractmethod
from typing import override

from .protocol import Auditable, AuditorProtocol


class AbstractAuditor(ABC, AuditorProtocol):
    """ABC for auditor."""

    @override
    @abstractmethod
    def record(
        self,
        step_name: str,
        obj: Auditable | None = None,
        **kwargs: object,
    ) -> None:
        """Record the attributes."""
