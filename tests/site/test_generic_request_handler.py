"""Generic request handler test."""

from typing import TypeVar
from unittest.mock import Mock

import pytest

from wse.application.protocols import Executable
from wse.site.handlers import ExerciseHandler
from wse.site.protocols import Preparable, ResponseAdaptable, Validatable

RequestParamsT = TypeVar('RequestParamsT')
RequestContextT = TypeVar('RequestContextT')
RequestDataT = TypeVar('RequestDataT')

ValidatedT = TypeVar('ValidatedT')
CommandT = TypeVar('CommandT')
ResultT = TypeVar('ResultT')
AdaptedT = TypeVar('AdaptedT')


# Data mocking


@pytest.fixture
def mock_request_params() -> Mock:
    """Provide a request parameters mock."""
    return Mock()


@pytest.fixture
def mock_request_context() -> Mock:
    """Provide a request context mock."""
    return Mock()


@pytest.fixture
def mock_request_data() -> Mock:
    """Provide a request data mock."""
    return Mock()


@pytest.fixture
def mock_validated() -> Mock:
    """Provide a validated data mock."""
    return Mock()


@pytest.fixture
def mock_command() -> Mock:
    """Provide a command mock."""
    return Mock()


@pytest.fixture
def mock_result() -> Mock:
    """Provide a use case execute result."""
    return Mock()


# Dependency mocking


@pytest.fixture
def mock_validator(
    mock_validated: Mock,
) -> Mock:
    """Provide a request data validator mock."""
    mock = Mock(spec=Validatable)
    mock.validate.return_value = mock_validated
    return mock


@pytest.fixture
def mock_assembler(
    mock_command: Mock,
) -> Mock:
    """Provide a create use case command assembler mock."""
    mock = Mock(spec=Preparable)
    mock.prepare.return_value = mock_command
    return mock


@pytest.fixture
def mock_use_case(
    mock_result: Mock,
) -> Mock:
    """Provide an use case mock."""
    mock = Mock(spec=Executable)
    mock.execute.return_value = mock_result
    return mock


@pytest.fixture
def mock_adapter() -> Mock:
    """Provide a request handling result adapter mock."""
    mock = Mock(spec=ResponseAdaptable)
    return mock


# Tested handler


@pytest.fixture
def handler(
    mock_validator: Validatable[RequestDataT, ValidatedT],
    mock_assembler: Preparable[
        RequestParamsT, RequestContextT, ValidatedT, CommandT
    ],
    mock_use_case: Executable[CommandT, ResultT],
    mock_adapter: ResponseAdaptable[ResultT, RequestContextT, AdaptedT],
) -> ExerciseHandler[
    RequestParamsT,
    RequestContextT,
    RequestDataT,
    ValidatedT,
    CommandT,
    ResultT,
    AdaptedT,
]:
    """Provide a request handler."""
    return ExerciseHandler(
        validator=mock_validator,
        assembler=mock_assembler,
        use_case=mock_use_case,
        adapter=mock_adapter,
    )


# Test


def test_request_handler_dependencies_called(
    mock_validator: Mock,
    mock_assembler: Mock,
    mock_use_case: Mock,
    mock_adapter: Mock,
    handler: ExerciseHandler[Mock, Mock, Mock, Mock, Mock, Mock, Mock],
    mock_request_params: Mock,
    mock_request_context: Mock,
    mock_request_data: Mock,
    mock_validated: Mock,
    mock_command: Mock,
    mock_result: Mock,
) -> None:
    # Act
    handler.handle(
        mock_request_params,
        mock_request_context,
        mock_request_data,
    )

    # Assert
    mock_validator.validate.assert_called_once_with(
        mock_request_data,
    )
    mock_assembler.prepare.assert_called_once_with(
        mock_request_params,
        mock_request_context,
        mock_validated,
    )
    mock_use_case.execute.assert_called_once_with(
        mock_command,
    )
    mock_adapter.to_response.assert_called_once_with(
        mock_result,
        mock_request_context,
    )
