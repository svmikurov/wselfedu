"""Generic exercise use case test configuration."""

from unittest.mock import Mock

import pytest

from apps.core.assemblers.command import UserDataCommand
from apps.core.domains.exercise.dto import (
    ExerciseDomainResultDTO,
    ExerciseSpecDTO,
)
from apps.core.domains.exercise.enums import (
    ExerciseProcessEnum,
    ExerciseStatusEnum,
)
from apps.core.exceptions.storage import StorageMissError
from apps.core.services.protocol import UserServiceProtocol
from apps.core.use_cases.exercise.generic import ExerciseUseCaseStrategy
from apps.core.validators.request.dto import ExerciseActionWebDTO
from apps.users.models import Person

from ._types import (
    AdapterT,
    BuilderT,
    CaseT,
    ResolverT,
    ResultT,
    ServiceT,
    StorageT,
    UseCaseT,
)

STORE_PREFIX = 'test_prefix'

# =================================================
# Commands
# =================================================


@pytest.fixture
def create_command(
    mock_person: Person,
) -> UserDataCommand[ExerciseActionWebDTO]:
    """Provide create exercise command fixture."""
    return UserDataCommand(
        user=mock_person,
        data=ExerciseActionWebDTO(
            action=ExerciseProcessEnum.CREATE_CASE,
        ),
    )


# =================================================
# Inner DTOs
# =================================================


@pytest.fixture
def stored_case() -> CaseT:
    """Provide stored case mock."""
    return Mock(spec=CaseT)


@pytest.fixture
def current_case() -> CaseT:
    """Provide current case mock."""
    return Mock(spec=ExerciseDomainResultDTO)


@pytest.fixture
def mock_params() -> Mock:
    """Provide exercise parameters mock."""
    return Mock()


@pytest.fixture
def mock_spec() -> Mock:
    """Provide spec mock."""
    return Mock(spec=ExerciseSpecDTO)


@pytest.fixture
def mock_domain_result(
    current_case: Mock,
) -> Mock:
    """Provide spec mock."""
    mock = Mock(spec=ExerciseDomainResultDTO)
    mock.status = ExerciseStatusEnum.NEW_TASK
    mock.case = current_case
    return mock


@pytest.fixture
def mock_use_case_result() -> ResultT:
    """Provide spec mock."""
    return Mock(spec=ResultT)


# =================================================
# Use case dependencies
# =================================================


@pytest.fixture
def mock_empty_storage() -> StorageT:
    """Provide storage mock."""
    mock = Mock(spec=StorageT)
    mock.retrieve.side_effect = StorageMissError('No case')
    return mock


@pytest.fixture
def mock_storage(
    stored_case: CaseT,
) -> StorageT:
    """Provide storage mock."""
    mock = Mock(spec=StorageT)
    mock.retrieve.return_value = stored_case
    return mock


@pytest.fixture
def mock_config_resolver(
    mock_params: Mock,
) -> ResolverT:
    """Provide config resolver mock."""
    mock = Mock(spec=ResolverT)
    mock.resolve.return_value = mock_params
    return mock


# =================================================
# Use case strategy dependencies
# =================================================


@pytest.fixture
def mock_create_adapter(mock_spec: Mock) -> AdapterT:
    """Provide create exercise case adapter mock."""
    mock = Mock(spec=AdapterT)
    mock.adapt.return_value = mock_spec
    return mock


@pytest.fixture
def mock_create_service(
    mock_domain_result: Mock,
) -> ServiceT:
    """Provide create exercise case service mock."""
    mock = Mock(spec=UserServiceProtocol)
    mock.execute.return_value = mock_domain_result
    return mock


@pytest.fixture
def mock_create_builder(
    mock_use_case_result: Mock,
) -> BuilderT:
    """Provide create exercise case builder mock."""
    mock = Mock(spec=BuilderT)
    mock.build.return_value = mock_use_case_result
    return mock


# =================================================
# Use case strategy registries
# =================================================


@pytest.fixture
def mock_adapter_registry(
    mock_create_adapter: AdapterT,
) -> dict[ExerciseProcessEnum, AdapterT]:
    """Provide mocked adapter mock registry."""
    return {
        ExerciseProcessEnum.CREATE_CASE: mock_create_adapter,
    }


@pytest.fixture
def mock_service_registry(
    mock_create_service: ServiceT,
) -> dict[ExerciseProcessEnum, ServiceT]:
    """Provide mocked service mock registry."""
    return {
        ExerciseProcessEnum.CREATE_CASE: mock_create_service,
    }


@pytest.fixture
def mock_builder_registry(
    mock_create_builder: BuilderT,
) -> dict[ExerciseStatusEnum, BuilderT]:
    """Provide mocked builder mock registry."""
    return {
        ExerciseStatusEnum.NEW_TASK: mock_create_builder,
    }


# =================================================
# Use case strategy
# =================================================


@pytest.fixture
def use_case(
    mock_empty_storage: Mock,
    mock_config_resolver: ResolverT,
    mock_adapter_registry: dict[ExerciseProcessEnum, AdapterT],
    mock_service_registry: dict[ExerciseProcessEnum, ServiceT],
    mock_builder_registry: dict[ExerciseStatusEnum, BuilderT],
) -> UseCaseT:
    """Provide generic exercise use case fixture."""
    return ExerciseUseCaseStrategy(
        prefix=STORE_PREFIX,
        storage=mock_empty_storage,
        config_resolver=mock_config_resolver,
        adapter_registry=mock_adapter_registry,
        service_registry=mock_service_registry,
        builder_registry=mock_builder_registry,
    )
