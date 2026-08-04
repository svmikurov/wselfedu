"""Domain model fixtures."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from unittest.mock import Mock

import pytest

from wse.domain import commands, factories, model
from wse.domain.protocols import Executable

SESSION_ID = 'session_id_123'
QUESTION_TEXT = 'question_text'

if TYPE_CHECKING:
    from typing import TypeAlias

    from wse.domain.protocols import ExerciseProtocol, TaskProtocol

    AggregateT: TypeAlias = ExerciseProtocol[Any, Any, Any, Any, Any]


@pytest.fixture
def task() -> TaskProtocol:
    """Provide a task."""
    return model.Task(question_text=QUESTION_TEXT)


@pytest.fixture
def create_task_command() -> commands.Command:
    """Provide a check answer command."""
    return commands.CreateTask(
        session_id=SESSION_ID,
    )


@pytest.fixture
def check_answer_command() -> commands.Command:
    """Provide a check answer command."""
    return commands.Command()


@pytest.fixture
def mock_create_strategy(task: TaskProtocol) -> Mock:
    """Provide a mock for create task strategy."""
    mock = Mock(spec=Executable)
    mock.execute.return_value = task
    return mock


@pytest.fixture
def mock_check_strategy() -> Mock:
    """Provide a mock for check answer strategy."""
    return Mock(spec=Executable)


@pytest.fixture
def exercise(
    mock_create_strategy: Mock, mock_check_strategy: Mock,
) -> AggregateT:
    """Provide an exercise instance with mocked strategies."""
    factory = factories.ExerciseFactory(
        create_strategy=mock_create_strategy,
        check_strategy=mock_check_strategy,
    )
    return factory.create(session_id=SESSION_ID)
