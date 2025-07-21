"""Defines tests configuration."""

import pytest

from unittest.mock import Mock

from .._abc_input import ICalculatorService
from .._abc_output import IOutputPort
from ..adapter import ConsoleOutputAdapter
from ..core import CalculatorCore


@pytest.fixture
def console_output() -> IOutputPort:
    """Fixture providing console output adapter."""
    return ConsoleOutputAdapter()


@pytest.fixture
def calculator(console_output: IOutputPort) -> ICalculatorService:
    """Fixture providing calculator."""
    return CalculatorCore(console_output)


@pytest.fixture()
def mock_output() -> IOutputPort:
    """Fixture providing output mock."""
    return Mock(spec=IOutputPort)


@pytest.fixture
def calculator_mock_output(mock_output: Mock) -> ICalculatorService:
    """Fixture providing calculator."""
    return CalculatorCore(mock_output)


