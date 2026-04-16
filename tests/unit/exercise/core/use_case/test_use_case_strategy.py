"""Core exercise use case strategy tests."""

from typing import Any
from unittest.mock import Mock

import pytest

from apps.core.adapters.exercise.protocol import ExerciseProcessAdapterProtocol
from apps.core.assemblers.protocol import UserDataCommandProtocol
from apps.core.domains.exercise.enums import (
    ExerciseProcessEnum,
    ExerciseStatusEnum,
)
from apps.core.domains.exercise.protocol import (
    ExerciseConfigProtocol,
    ExerciseParametersProtocol,
    ExerciseProcessResultProtocol,
    HasExerciseProcessAction,
    HasExerciseStatus,
)
from apps.core.domains.task.protocol import TaskBuilderProtocol
from apps.core.services.protocol import UserServiceProtocol
from apps.core.use_cases.exercise.generic import ExerciseUseCaseStrategy
from apps.core.use_cases.protocol import UseCaseProtocol

CommandT = UserDataCommandProtocol[HasExerciseProcessAction]
CaseT = HasExerciseStatus
# FIXME: Fix Any type hint after type definition
SpecT = Any
ResultT = Any
UseCaseT = UseCaseProtocol[CommandT, HasExerciseStatus]
AdapterT = ExerciseProcessAdapterProtocol[
    CommandT, ExerciseParametersProtocol, CaseT | None, SpecT
]
ServiceT = UserServiceProtocol[SpecT, ExerciseProcessResultProtocol[CaseT]]
BuilderT = TaskBuilderProtocol[
    ExerciseProcessResultProtocol[CaseT],
    ExerciseConfigProtocol,
    ResultT,
]

# =================================================
# UseCase's dependency mock
# =================================================


@pytest.fixture
def mock_create_task_adapter() -> AdapterT:
    """Provide create task adapter."""
    mock = Mock(spec=AdapterT)
    return mock


@pytest.fixture
def mock_create_task_service() -> ServiceT:
    """Provide create task service."""
    mock = Mock(spec=ServiceT)
    result = Mock(spec=ExerciseProcessResultProtocol)
    result.status = ExerciseStatusEnum.NEW_TASK
    result.case = Mock()
    mock.execute.return_value = result
    return mock


@pytest.fixture
def mock_create_task_builder() -> BuilderT:
    """Provide create task builder."""
    mock = Mock(spec=BuilderT)
    return mock


# =================================================
# UseCase's dependency registry mock
# =================================================


@pytest.fixture
def mock_adapter_registry(
    mock_create_task_adapter: AdapterT,
) -> dict[ExerciseProcessEnum, AdapterT]:
    """Provide adapter registry."""
    return {
        ExerciseProcessEnum.CREATE_CASE: mock_create_task_adapter,
    }


@pytest.fixture
def mock_service_registry(
    mock_create_task_service: ServiceT,
) -> dict[ExerciseProcessEnum, ServiceT]:
    """Provide service registry."""
    return {
        ExerciseProcessEnum.CREATE_CASE: mock_create_task_service,
    }


@pytest.fixture
def mock_builder_registry(
    mock_create_task_builder: BuilderT,
) -> dict[ExerciseStatusEnum, BuilderT]:
    """Provide builder registry."""
    return {
        ExerciseStatusEnum.NEW_TASK: mock_create_task_builder,
    }


# =================================================
# UseCase strategy mock
# =================================================


@pytest.fixture
def use_case(
    mock_adapter_registry: dict[ExerciseProcessEnum, AdapterT],
    mock_service_registry: dict[ExerciseProcessEnum, ServiceT],
    mock_builder_registry: dict[ExerciseStatusEnum, BuilderT],
) -> UseCaseT:
    """Provide exercise use case strategy fixture with mock."""
    return ExerciseUseCaseStrategy(
        prefix='test',
        storage=Mock(),
        config_resolver=Mock(),
        adapter_registry=mock_adapter_registry,
        service_registry=mock_service_registry,
        builder_registry=mock_builder_registry,
    )


# =================================================
# Tests
# =================================================


# TODO: Extend test case coverage
class TestExerciseUseCaseStrategy:
    """Exercise use case strategy test."""

    def test_initialize_use_case(
        self,
        use_case: UseCaseT,
    ) -> None:
        """Test that use case has been initialized successfully."""
        assert use_case is not None, 'Use case was not initialized'

    @pytest.mark.django_db
    def test_new_case_command(
        self,
        use_case: UseCaseT,
        new_case_command: CommandT,
        mock_create_task_adapter: AdapterT,
        mock_create_task_service: ServiceT,
        mock_create_task_builder: BuilderT,
    ) -> None:
        """Test use case dependencies call."""
        # Act
        use_case.execute(new_case_command)

        # Assert
        mock_create_task_adapter.adapt.assert_called_once()  # type: ignore[attr-defined]
        mock_create_task_service.execute.assert_called_once()  # type: ignore[attr-defined]
        mock_create_task_builder.build.assert_called_once()  # type: ignore[attr-defined]
