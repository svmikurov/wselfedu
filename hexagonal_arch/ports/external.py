"""Defines ports to output data."""

from abc import ABC, abstractmethod


class IOutputPort(ABC):
    """Interface for output handling."""

    @abstractmethod
    def show_result(self, result: float) -> None:
        """Display calculation result."""


class IHistoryRepository(ABC):
    """Interface for operation history storage."""

    @abstractmethod
    def save(
        self, operation: str, op1: float, op2: float, result: float
    ) -> None:
        """Save operation details."""
