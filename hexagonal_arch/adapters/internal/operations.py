"""Defines adapters."""

from ...enums import CalculateEnum
from ...factories.operation import OperationFactory
from ...ports.internal import IOperation


@OperationFactory.register(CalculateEnum.ADD)
class AddOperation(IOperation):
    """Addition operation implementation."""

    def execute(self, op1: float, op2: float) -> float:
        """Execute adding operation."""
        return op1 + op2


@OperationFactory.register(CalculateEnum.SUBTRACT)
class SubtractOperation(IOperation):
    """Substation operation implementation."""

    def execute(self, op1: float, op2: float) -> float:
        """Execute subtract operation."""
        return op1 - op2


@OperationFactory.register(CalculateEnum.DIVIDE)
class DivideOperation(IOperation):
    """Division operation implementation."""

    def execute(self, op1: float, op2: float) -> float:
        """Execute divide operation."""
        if op2 == 0:
            raise ValueError('Division by zero')
        return op1 / op2


@OperationFactory.register(CalculateEnum.MULTIPLY)
class MultiplyOperation(IOperation):
    """Multiplication operation implementation."""

    def execute(self, op1: float, op2: float) -> float:
        """Execute multiply operation."""
        return op1 * op2
