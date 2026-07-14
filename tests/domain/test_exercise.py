"""Exercise tests."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from unittest.mock import Mock

import pytest

from wse.domain import commands, events, factories, models
from wse.domain.protocols import Executable

if TYPE_CHECKING:
    from wse.domain.protocols import ExerciseProtocol, TaskProtocol

SESSION_ID = 'session_id_123'
QUESTION_TEXT = 'question_text'


@pytest.fixture
def task() -> TaskProtocol:
    """Provide a task."""
    return models.Task(question_text=QUESTION_TEXT)


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
def exercise(
    create_strategy: Mock, check_strategy: Mock
) -> ExerciseProtocol[Any]:
    """Provide an exercise instance with mocked strategies."""
    factory = factories.ExerciseFactory(
        create_strategy=create_strategy,
        check_strategy=check_strategy,
    )
    return factory.create(session_id=SESSION_ID)


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
    assert isinstance(exercise, models.Exercise), (
        'Factory should return Exercise instance'
    )

    # Assert: Session ID set correctly
    assert exercise._session_id == SESSION_ID, 'Session ID not set correctly'

    # Assert: Task not created yet
    with pytest.raises(RuntimeError, match='No task has been created yet'):
        _ = exercise.task


def test_create_task_creates_task_and_emits_event(
    create_strategy: Mock,
    check_strategy: Mock,
    exercise: ExerciseProtocol[Any],
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
    exercise: ExerciseProtocol[Any],
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
    exercise: ExerciseProtocol[Any],
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
    exercise: ExerciseProtocol[Any],
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
