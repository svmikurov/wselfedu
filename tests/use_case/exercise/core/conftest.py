"""Generic exercise use case test configuration."""

from unittest.mock import Mock

import pytest

from apps.core.assemblers.command import UserDataCommand
from apps.core.exceptions.storage import StorageMissError
from apps.core.services.protocol import UserServiceProtocol
from apps.core.use_cases.exercise.generic import ExerciseUseCaseStrategy
from apps.users.models import Person
from contracts.entity.domain.exercise import flow
from contracts.schemas.domain.exercise.params import (
    ExerciseSpecDTO,
)
from contracts.schemas.request.exercise import ExerciseRequestDTO
from ports.contract.enums.exercise import (
    ExerciseAction,
    ExerciseStatus,
)

from ._types import (
    BuilderT,
    CaseT,
    ResolverT,
    ResultT,
    ServiceT,
    SpecFactoryT,
    StorageT,
    UseCaseT,
)

STORE_PREFIX = 'test_prefix'

# =================================================
# Commands
# =================================================


@pytest.fixture
def create_command(
    mock_user: Person,
) -> UserDataCommand[ExerciseRequestDTO]:
    """Provide create exercise command fixture."""
    return UserDataCommand(
        user=mock_user,
        data=ExerciseRequestDTO(
            action=ExerciseAction.CREATE_TASK,
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
def domain_result() -> CaseT:
    """Provide exercise domain result mock."""
    return Mock(spec=flow.ExerciseDomainResultProtocol)


@pytest.fixture
def mock_params() -> Mock:
    """Provide exercise parameters mock."""
    return Mock()


@pytest.fixture
def mock_spec() -> Mock:
    """Provide spec mock."""
    return Mock(spec=ExerciseSpecDTO)


@pytest.fixture
def mock_case(
    domain_result: Mock,
) -> Mock:
    """Provide exercise case mock."""
    mock = Mock(spec=flow.ExerciseCaseProtocol)
    mock.status = ExerciseStatus.NEW_TASK
    mock.domain = domain_result
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
def mock_spec_factory(mock_spec: Mock) -> SpecFactoryT:
    """Provide create exercise specification factory mock."""
    mock = Mock(spec=SpecFactoryT)
    mock.create.return_value = mock_spec
    return mock


@pytest.fixture
def mock_create_service(
    mock_case: Mock,
) -> ServiceT:
    """Provide create exercise case service mock."""
    mock = Mock(spec=UserServiceProtocol)
    mock.execute.return_value = mock_case
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
def mock_spec_factory_registry(
    mock_spec_factory: SpecFactoryT,
) -> dict[ExerciseAction, SpecFactoryT]:
    """Provide specification factory mock registry."""
    return {
        ExerciseAction.CREATE_TASK: mock_spec_factory,
    }


@pytest.fixture
def mock_service_registry(
    mock_create_service: ServiceT,
) -> dict[ExerciseAction, ServiceT]:
    """Provide mocked service mock registry."""
    return {
        ExerciseAction.CREATE_TASK: mock_create_service,
    }


@pytest.fixture
def mock_builder_registry(
    mock_create_builder: BuilderT,
) -> dict[ExerciseStatus, BuilderT]:
    """Provide mocked builder mock registry."""
    return {
        ExerciseStatus.NEW_TASK: mock_create_builder,
    }


# =================================================
# Use case strategy
# =================================================


@pytest.fixture
def use_case(
    mock_empty_storage: Mock,
    mock_config_resolver: ResolverT,
    mock_spec_factory_registry: dict[ExerciseAction, SpecFactoryT],
    mock_service_registry: dict[ExerciseAction, ServiceT],
    mock_builder_registry: dict[ExerciseStatus, BuilderT],
) -> UseCaseT:
    """Provide generic exercise use case fixture."""
    return ExerciseUseCaseStrategy(
        prefix=STORE_PREFIX,
        storage=mock_empty_storage,
        config_resolver=mock_config_resolver,
        spec_factory_registry=mock_spec_factory_registry,
        service_registry=mock_service_registry,
        builder_registry=mock_builder_registry,
    )
