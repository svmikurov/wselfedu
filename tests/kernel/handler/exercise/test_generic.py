"""Generic request handler tests."""

from unittest.mock import Mock

import pytest

from kernel.handler.generic import RequestHandler
from tests.types.handler import (
    AdapterT,
    AssemblerT,
    CommandDataT,
    HandlerT,
    RequestContextT,
    RequestDataT,
    RequestParamsT,
    ResponseDataT,
    UseCaseResultT,
    UseCaseT,
    ValidatedT,
    ValidatorT,
)


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


def test_dependencies_called(
    # Request's data
    mock_request_params: RequestParamsT,
    mock_request_context: RequestContextT,
    mock_request_data: RequestDataT,
    # Inner data
    mock_validated: ValidatedT,
    mock_command: CommandDataT,
    mock_use_case_result: UseCaseResultT,
    # Handler's dependencies & Handler
    mock_assembler: Mock,
    mock_use_case: Mock,
    mock_adapter: Mock,
    handler: HandlerT,
) -> None:
    """Test that handler dependencies was called."""
    # Act
    handler.execute(
        mock_request_params,
        mock_request_context,
        mock_request_data,
    )

    # Assert
    mock_assembler.prepare.assert_called_once_with(
        mock_request_params,
        mock_request_context,
        mock_validated,
    )
    mock_use_case.execute.assert_called_once_with(
        mock_command,
    )
    mock_adapter.to_response.assert_called_once_with(
        mock_use_case_result,
        mock_request_context,
    )


def test_execute_successfully(
    mock_response_data: ResponseDataT,
    handler: HandlerT,
) -> None:
    """Test that handler execute was completed successfully."""
    # Act & Assert
    assert handler.execute(Mock(), Mock(), Mock()) == mock_response_data


def test_handler_initialized_successfully(
    handler: HandlerT,
) -> None:
    """Test that handler has ben initialized successfully."""
    # Assert
    assert handler is not None
