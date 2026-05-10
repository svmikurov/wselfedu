"""Generic request handler test configuration."""

from unittest.mock import Mock

import pytest

from apps.core.assemblers.command import UserDataCommand
from apps.core.handlers.dto import RequestContext, RequestData
from apps.core.handlers.generic import RequestHandler
from apps.users.models.user import Person
from contracts.schemas.domain.exercise.params import ExerciseSpecDTO
from di import MainContainer
from interfaces.protocols.command.exercise import (
    CheckTestCommandProtocol,
    CreateTaskCommandProtocol,
)
from interfaces.schemas.validator.task import (
    ValidatedCheckTestAnswer,
    ValidatedCreateTask,
)
from ports.contract.enums import ExerciseAction
from tests.fixtures.exercise.lang.no_db.translations import TRANSLATION_INDEX
from tests.types.handler import (
    AdapterT,
    AssemblerT,
    HandlerT,
    RequestContextT,
    RequestDataT,
    UseCaseT,
    ValidatorT,
)

from ._types import (
    CheckRequestDataT,
    CreateRequestDataT,
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


# Request context
# ---------------


@pytest.fixture
def request_context(
    user: Person,
) -> RequestContextT:
    """Provide request parameters DTO fixture."""
    return RequestContext(user=user)


# Request data
# ------------


@pytest.fixture
def create_task_request_data() -> CreateRequestDataT:
    """Provide create exercise request's data DTO."""
    # Request data DTO creates in view's method with GET request.
    return RequestData(
        data={
            'action': ExerciseAction.CREATE_TASK,
        },
    )


@pytest.fixture
def check_test_answer_request_data() -> CheckRequestDataT:
    """Provide check exercise request's data DTO."""
    # Request data DTO creates in view's method with GET request.
    return RequestData(
        data={
            'action': ExerciseAction.CHECK_ANSWER,
            'option_value': str(TRANSLATION_INDEX),
        },
    )


@pytest.fixture
def update_progress_request_data(user: Person) -> RequestDataT:
    """Provide *update progress* request data fixture."""
    return RequestData(
        data={
            'action': ExerciseAction.UPDATE_PROGRESS,
            'is_known': 'true',
        }
    )


# Mocks
# -----


@pytest.fixture
def mock_request_params() -> Mock:
    """Provide request parameters DTO mock."""
    return Mock()


@pytest.fixture
def mock_request_context(
    mock_user: Person,
) -> Mock:
    """Provide request context DTO mock."""
    mock = Mock()
    mock.user.return_value = mock_user
    return mock


@pytest.fixture
def mock_request_data() -> Mock:
    """Provide request data DTO mock."""
    return Mock()


# =================================================
# Validated data
# =================================================


@pytest.fixture
def validated_create() -> ValidatedCreateT:
    """Provide the *create task* DTO validated request data."""
    return ValidatedCreateTask(
        action=ExerciseAction.CREATE_TASK,
    )


@pytest.fixture
def validated_check() -> ValidatedCheckT:
    """Provide the *check test answer* DTO validated request data."""
    return ValidatedCheckTestAnswer(
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
        data=ValidatedCreateTask(
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
        data=ValidatedCheckTestAnswer(
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
