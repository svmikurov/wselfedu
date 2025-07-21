"""Defines ports for input data."""

from abc import ABC, abstractmethod


class ICalculatorService(ABC):
    """Input data port."""

    @abstractmethod
    def add(self, op1: float, op2: float) -> float:
        """Calculate the addition."""
        pass

    @abstractmethod
    def sub(self, op1: float, op2: float) -> float:
        """Calculate the subtraction."""
        pass

    @abstractmethod
    def mul(self, op1: float, op2: float) -> float:
        """Calculate the multiplication."""
        pass

    @abstractmethod
    def div(self, op1: float, op2: float) -> float:
        """Calculate the division."""
        pass
