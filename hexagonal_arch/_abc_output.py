"""Defines ports to output data."""

from abc import ABC, abstractmethod


class IOutputPort(ABC):
    """Output data port."""

    @abstractmethod
    def show_result(self, result: float) -> None:
        """Show result for external client."""
        pass
