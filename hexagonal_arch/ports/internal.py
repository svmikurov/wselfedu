"""Defines ports for input data."""

from abc import ABC, abstractmethod


class IOperation(ABC):
    """Interface for calculation operations."""

    @abstractmethod
    def execute(self, op1: float, op2: float) -> float:
        """Execute operation on two operands."""


class IValidator(ABC):
    """Interface for input validation."""

    @abstractmethod
    def validate(self, op1: float, op2: float) -> None:
        """Validate input operands."""
