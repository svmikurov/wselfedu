"""Defines validator."""

from ...ports.internal import IValidator


class OverflowValidator(IValidator):
    """Input overflow validation."""

    MAX = 10**6

    def validate(self, op1: float, op2: float) -> None:
        """Validate."""
        if op1 > self.MAX or op2 > self.MAX:
            raise ValueError('Values are too large')
