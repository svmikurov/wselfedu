"""Exercise aggregate tests."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from unittest.mock import Mock

import pytest

from tests.fixtures.exercise import QUESTION_TEXT, SESSION_ID
from wse.domain import commands, events, factories, model
from wse.domain.protocols import Executable

if TYPE_CHECKING:
    from typing import TypeAlias

    from wse.domain.protocols import ExerciseProtocol, TaskProtocol

    AggregateT: TypeAlias = ExerciseProtocol[Any, Any, Any, Any, Any]


@pytest.fixture
def create_strategy(task: TaskProtocol) -> Mock:
    """Provide a mock for create task strategy."""
    mock = Mock(spec=Executable)
    mock.execute.return_value = task
    return mock


@pytest.fixture
def check_strategy() -> Mock:
    """Provide a mock for check answer strategy."""
    return Mock(spec=Executable)


@pytest.fixture
def check_answer_command() -> commands.Command:
    """Provide a check answer command."""
    return commands.Command()


def test_factory_creates_exercise_with_session_id(
    create_strategy: Mock,
    check_strategy: Mock,
) -> None:
    # Arrange
    factory = factories.ExerciseFactory(
        create_strategy=create_strategy,
        check_strategy=check_strategy,
    )

    # Act
    exercise = factory.create(session_id=SESSION_ID)

    # Assert: Exercise instance created
    assert isinstance(exercise, model.Exercise), (
        'Factory should return Exercise instance'
    )

    # Assert: Session ID set correctly
    assert exercise._session_id == SESSION_ID, 'Session ID not set correctly'

    # Assert: Task not created yet
    with pytest.raises(RuntimeError, match='No task has been created yet'):
        _ = exercise.task


def test_create_task_creates_task_and_emits_event(
    exercise: AggregateT,
    create_strategy: Mock,
    check_strategy: Mock,
) -> None:
    # Act
    exercise.create_task()

    # Assert: Create strategy called once
    create_strategy.execute.assert_called_once()

    # Assert: Check strategy not called
    check_strategy.execute.assert_not_called()

    # Assert: Task created event added
    task_created_events = [
        e for e in exercise.events if isinstance(e, events.TaskCreated)
    ]
    assert len(task_created_events) == 1

    # Assert: Task has question text
    assert exercise.task.question_text == QUESTION_TEXT


def test_check_answer_emits_verified_event_on_correct_answer(
    exercise: AggregateT,
    check_strategy: Mock,
    check_answer_command: commands.Command,
) -> None:
    # Arrange
    check_strategy.execute.return_value = True

    # Act
    exercise.check_answer(check_answer_command)

    # Assert: Answer is marked correct
    assert exercise.is_correct_answer is True

    # Assert: Answer verified event added
    task_checked_events = [
        e for e in exercise.events if isinstance(e, events.AnswerVerified)
    ]
    assert len(task_checked_events) == 1


def test_check_answer_emits_incorrect_answer_event(
    exercise: AggregateT,
    check_strategy: Mock,
    check_answer_command: commands.Command,
) -> None:
    # Arrange
    check_strategy.execute.return_value = False

    # Act
    exercise.check_answer(check_answer_command)

    # Assert: Answer is marked incorrect
    assert exercise.is_correct_answer is False

    # Assert: Incorrect answer given event added
    task_checked_events = [
        e
        for e in exercise.events
        if isinstance(e, events.IncorrectAnswerGiven)
    ]
    assert len(task_checked_events) == 1


def test_check_answer_emits_task_created_on_correct_answer(
    exercise: AggregateT,
    check_strategy: Mock,
    check_answer_command: commands.Command,
) -> None:
    # Arrange: Answer is correct
    check_strategy.execute.return_value = True

    # Act
    exercise.check_answer(check_answer_command)

    # Assert: Task created event added
    task_created_events = [
        e for e in exercise.events if isinstance(e, events.TaskCreated)
    ]
    assert len(task_created_events) == 1


def test_task_created_event_popped(
    exercise: AggregateT,
) -> None:
    # Arrange: Add task created event
    exercise.create_task()

    # Act
    event = exercise.pop_event()

    # Assert
    assert isinstance(event, events.TaskCreated)
