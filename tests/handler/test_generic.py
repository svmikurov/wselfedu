"""Generic request handler tests."""

from unittest.mock import Mock

from .._types.handler import (
    CommandDataT,
    HandlerT,
    RequestContextT,
    RequestDataT,
    RequestParamsT,
    ResponseDataT,
    UseCaseResultT,
    ValidatedT,
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
