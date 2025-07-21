"""Defines tests for operations."""

import pytest

from ..adapters.external.output import ConsoleOutput
from ..adapters.external.repositories import PostgresHistoryRepository
from ..adapters.internal.validators import OverflowValidator
from ..core import CalculatorCore
from ..enums import CalculateEnum
from ..factories.operation import OperationFactory

calculator = CalculatorCore(
    operations=OperationFactory.create_operations(),
    validator=OverflowValidator(),
    output=ConsoleOutput(),
    history_repo=PostgresHistoryRepository(),
)


@pytest.mark.skip
def test_calculate() -> None:
    """Test the calculation."""
    assert calculator.calculate(CalculateEnum.ADD, 5, 3) == 8
    assert calculator.add(5, 3) == 8
    assert calculator.div(6, 3) == 2
    assert calculator.mul(6, 3) == 18
    assert calculator.sub(6, 3) == 3
