"""Defines core calculation logic."""

from ._abc_input import ICalculatorService
from ._abc_output import IOutputPort


class CalculatorCore(ICalculatorService):
    """Core calculation logic."""

    def __init__(
        self,
        output: IOutputPort,
    ) -> None:
        """Construct the service."""
        self._output = output

    def add(self, op1: float, op2: float) -> float:
        """Calculate the addition."""
        result = op1 + op2
        self._output.show_result(result)
        return result

    def sub(self, op1: float, op2: float) -> float:
        """Calculate the subtraction."""
        result = op1 - op2
        self._output.show_result(result)
        return result

    def mul(self, op1: float, op2: float) -> float:
        """Calculate the multiplication."""
        result = op1 * op2
        self._output.show_result(result)
        return result

    def div(self, op1: float, op2: float) -> float:
        """Calculate the division."""
        if op2 == 0:
            raise ValueError('Division by zero!')
        result = op1 / op2
        self._output.show_result(result)
        return result
