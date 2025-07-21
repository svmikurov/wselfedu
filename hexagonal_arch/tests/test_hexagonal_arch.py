"""Defines tests for hexagonal architecture components."""

import math
import sys
from io import StringIO
from unittest.mock import Mock

from .._abc_input import ICalculatorService


def test_add(calculator: ICalculatorService) -> None:
    """Test add calculator port."""
    fake_stdout = StringIO()
    sys.stdout = fake_stdout

    result = calculator.add(2, 3)

    assert result == 5.0

    sys.stdout = sys.__stdout__
    assert fake_stdout.getvalue().strip() == 'Result: 5'


def test_mock_output(
    mock_output: Mock,
    calculator_mock_output: ICalculatorService,
) -> None:
    """Test add calculator port."""
    result = calculator_mock_output.add(2, 2)

    assert result == 4.0
    mock_output.show_result.assert_called_once_with(4.0)


def test_combine_calculation(
    calculator: ICalculatorService,
) -> None:
    """Test the combined calculation."""
    result = calculator.add(calculator.div(8.0, 4), calculator.mul(3, 1.1))
    assert math.isclose(result, 5.3, rel_tol=1e-9)
