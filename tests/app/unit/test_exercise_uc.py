"""Exercise use case tests."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeAlias
from unittest.mock import Mock

import pytest

from wse.app.collectors import ExerciseResultCollector
from wse.app.protocols import Executable
from wse.app.use_cases import ExerciseUseCase

if TYPE_CHECKING:
    from wse.app.abstract import AbstractResultCollector
    from wse.domain.commands import TaskCommand
    from wse.domain.protocols import ExerciseProtocol

    UseCaseT: TypeAlias = Executable[Any, Any]
    AggregateT: TypeAlias = ExerciseProtocol[Any, Any, Any, Any, Any]


@pytest.fixture
def aggregate_factory_mock(exercise: AggregateT) -> Mock:
    """Provide a mock for aggregate factory."""
    mock = Mock()
    mock.create.return_value = exercise
    return mock


@pytest.fixture
def handlers_mock() -> Mock:
    """Provide a mock for exercise command handlers."""
    return Mock()


@pytest.fixture
def result_collector() -> AbstractResultCollector[Any, Any]:
    """Provide a use case result collector."""
    return ExerciseResultCollector()


@pytest.fixture
def exercise_use_case(
    aggregate_factory_mock: Mock,
    handlers_mock: Mock,
    result_collector: Mock,
) -> UseCaseT:
    """Provide a exercise use case with mocked dependencies."""
    return ExerciseUseCase(
        aggregate_factory=aggregate_factory_mock,
        handler_registry=handlers_mock,
        result_collector=result_collector,
    )


###################################################
# Tests
###################################################


def test_exercise_use_case_execute_creates_task(
    create_task_command: TaskCommand,
    exercise_use_case: UseCaseT,
) -> None:
    # Act
    result = exercise_use_case.execute(create_task_command)

    # Assert
    assert hasattr(result, 'task')
    assert result.task is not None
