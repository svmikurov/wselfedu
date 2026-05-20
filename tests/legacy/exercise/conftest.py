"""Generic request handler test configuration."""

from unittest.mock import Mock

import pytest

from apps.users.models.user import Person
from di import MainContainer
from kernel.handler.generic import RequestHandler
from ports.contract.enums import ExerciseAction
from ports.interfaces.protocols.command.exercise import (
    CheckTestCommandProtocol,
    CreateTaskCommandProtocol,
)
from ports.interfaces.schemas.command import UserDataCommand
from ports.interfaces.schemas.domain.exercise.params import ExerciseSpecDTO
from ports.interfaces.schemas.handler.task import (
    CheckTestAnswerSchema,
    CreateTaskSchema,
)
from tests.fixtures.exercise.lang.no_db.translations import TRANSLATION_INDEX
from tests.types.handler import (
    AdapterT,
    AssemblerT,
    HandlerT,
    UseCaseT,
    ValidatorT,
)

from ..._types import (
    ValidatedCheckT,
    ValidatedCreateT,
)

# =================================================
# Handler fixtures
# =================================================


@pytest.fixture
def regular_presentation_handler(
    main_container: MainContainer,
) -> HandlerT:
    """Provide translation regular presentation exercise handler."""
    return (  # type: ignore
        main_container.lang.handlers.regular_translation_presentation()  # type: ignore
    )


@pytest.fixture
def regular_test_handler(main_container: MainContainer) -> HandlerT:
    """Provide translation regular test exercise handler."""
    return (  # type: ignore
        main_container.lang.handlers.regular_translation_test()  # type: ignore
    )


# =================================================
# Request's DTOs
# =================================================


# Mocks
# -----

# =================================================
# Validated data
# =================================================


@pytest.fixture
def validated_create() -> ValidatedCreateT:
    """Provide the *create task* DTO validated request data."""
    return CreateTaskSchema(
        action=ExerciseAction.CREATE_TASK,
    )


@pytest.fixture
def validated_check() -> ValidatedCheckT:
    """Provide the *check test answer* DTO validated request data."""
    return CheckTestAnswerSchema(
        action=ExerciseAction.CHECK_ANSWER,
        option_value=TRANSLATION_INDEX,
    )


# =================================================
# Commands
# =================================================


@pytest.fixture
def create_task_command(
    user: Person,
) -> CreateTaskCommandProtocol:
    """Provide create exercise command fixture."""
    return UserDataCommand(
        user=user,
        data=CreateTaskSchema(
            action=ExerciseAction.CREATE_TASK,
        ),
    )


@pytest.fixture
def check_test_command(
    user: Person,
) -> CheckTestCommandProtocol:
    """Provide create exercise command fixture."""
    return UserDataCommand(
        user=user,
        data=CheckTestAnswerSchema(
            action=ExerciseAction.CHECK_ANSWER,
            option_value=TRANSLATION_INDEX,
        ),
    )


# =================================================
# Service specifications
# =================================================


@pytest.fixture
def mock_existing_case() -> Mock:
    """Provide exercise case mock."""
    return Mock()


@pytest.fixture
def create_task_spec(
    mock_existing_case: Mock,
) -> ExerciseSpecDTO[object]:
    """Provide the create test task service specification."""
    return ExerciseSpecDTO(
        case=mock_existing_case,
    )


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
