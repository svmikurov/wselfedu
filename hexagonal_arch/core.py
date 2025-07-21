"""Defines core calculation logic."""

from abc import ABC, abstractmethod
from typing import Dict

from .enums import CalculateEnum
from .ports.external import IHistoryRepository, IOutputPort
from .ports.internal import IOperation, IValidator


class ICalculator(ABC):
    """Core calculator interface."""

    @abstractmethod
    def calculate(
        self, operation: CalculateEnum, op1: float, op2: float
    ) -> float:
        """Perform calculation with given operation."""

    @abstractmethod
    def add(self, op1: float, op2: float) -> float:
        """Add."""

    @abstractmethod
    def sub(self, op1: float, op2: float) -> float:
        """Subtract."""

    @abstractmethod
    def mul(self, op1: float, op2: float) -> float:
        """Multiply."""

    @abstractmethod
    def div(self, op1: float, op2: float) -> float:
        """Divide."""


class CalculatorCore(ICalculator):
    """Core calculator implementation."""

    def __init__(
        self,
        operations: Dict[CalculateEnum, IOperation],
        validator: IValidator,
        output: IOutputPort,
        history_repo: IHistoryRepository,
    ) -> None:
        """Initialize with dependencies."""
        self._operations = operations
        self._validator = validator
        self._output = output
        self._history_repo = history_repo

    def calculate(
        self, operation: CalculateEnum, op1: float, op2: float
    ) -> float:
        """Perform calculation with given operation."""
        self._validator.validate(op1, op2)

        operation_type = self._operations[operation]
        result = operation_type.execute(op1, op2)

        self._history_repo.save(operation.value, op1, op2, result)
        self._output.show_result(result)

        return result

    def add(self, op1: float, op2: float) -> float:
        """Add."""
        return self.calculate(CalculateEnum.ADD, op1, op2)

    def sub(self, op1: float, op2: float) -> float:
        """Subtract."""
        return self.calculate(CalculateEnum.SUBTRACT, op1, op2)

    def mul(self, op1: float, op2: float) -> float:
        """Multiply."""
        return self.calculate(CalculateEnum.MULTIPLY, op1, op2)

    def div(self, op1: float, op2: float) -> float:
        """Divide."""
        return self.calculate(CalculateEnum.DIVIDE, op1, op2)
