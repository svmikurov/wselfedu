"""Abstract base class for auditor."""

from abc import ABC, abstractmethod
from typing import override

from .protocol import AuditorProtocol


class AbstractAuditor(ABC, AuditorProtocol):
    """ABC for auditor."""

    @override
    @abstractmethod
    def record(self, step_name: str, **kwargs: object) -> None:
        """Record the attributes."""
