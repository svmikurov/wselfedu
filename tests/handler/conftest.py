"""Generic request handler test configuration."""

from unittest.mock import Mock

import pytest

from apps.core.handlers.generic import RequestHandler

from .._types.handler import (
    AdapterT,
    AssemblerT,
    HandlerT,
    UseCaseT,
    ValidatorT,
)

# =================================================
# Request's DTOs
# =================================================


@pytest.fixture
def mock_request_params() -> Mock:
    """Provide request parameters DTO mock."""
    return Mock()


@pytest.fixture
def mock_request_context() -> Mock:
    """Provide request context DTO mock."""
    return Mock()


@pytest.fixture
def mock_request_data() -> Mock:
    """Provide request data DTO mock."""
    return Mock()


# =================================================
# Inner DTOs
# =================================================


@pytest.fixture
def mock_validated() -> Mock:
    """Provide validated request data DTO mock."""
    return Mock()


@pytest.fixture
def mock_command() -> Mock:
    """Provide command data DTO mock."""
    return Mock()


@pytest.fixture
def mock_use_case_result() -> Mock:
    """Provide use case result DTO mock."""
    return Mock()


# =================================================
# Outer DTO
# =================================================


@pytest.fixture
def mock_response_data() -> Mock:
    """Provide request handler response DTO mock."""
    return Mock()


# =================================================
# Handler's dependencies
# =================================================


@pytest.fixture
def mock_validator(
    mock_validated: Mock,
) -> ValidatorT:
    """Provide validator mock."""
    mock = Mock(spec=ValidatorT)
    mock.validate.return_value = mock_validated
    return mock


@pytest.fixture
def mock_assembler(
    mock_command: Mock,
) -> AssemblerT:
    """Provide assembler mock."""
    mock = Mock(spec=AssemblerT)
    mock.prepare.return_value = mock_command
    return mock


@pytest.fixture
def mock_use_case(
    mock_use_case_result: Mock,
) -> UseCaseT:
    """Provide use case mock."""
    mock = Mock(spec=UseCaseT)
    mock.execute.return_value = mock_use_case_result
    return mock


@pytest.fixture
def mock_adapter(
    mock_response_data: Mock,
) -> AdapterT:
    """Provide adapter mock."""
    mock = Mock(spec=AdapterT)
    mock.to_response.return_value = mock_response_data
    return mock


# =================================================
# Handler
# =================================================


@pytest.fixture
def handler(
    mock_validator: ValidatorT,
    mock_assembler: AssemblerT,
    mock_use_case: UseCaseT,
    mock_adapter: AdapterT,
) -> HandlerT:
    """Provide request handler fixture with mocked dependencies."""
    return RequestHandler(
        validator=mock_validator,
        assembler=mock_assembler,
        use_case=mock_use_case,
        adapter=mock_adapter,
    )
