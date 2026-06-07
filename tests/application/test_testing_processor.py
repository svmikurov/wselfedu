"""Testing process use case test."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from wse.application.use_case import ExerciseProcessor
from wse.domain.commands import CheckAnswerCommand, CreateTaskCommand

if TYPE_CHECKING:
    from wse.application.abstract import (
        AbstractCheckAnswerUseCase,
        AbstractCreateTaskUseCase,
        AbstractExerciseUseCase,
    )
    from wse.application.protocols import ExecutableExercise
    from wse.domain.protocols import CheckableOption, HasCorrect, Testable


@pytest.fixture
def testing_processor(
    create_testing_task_use_case: AbstractCreateTaskUseCase[Testable],
    check_testing_answer_use_case: AbstractCheckAnswerUseCase[
        CheckableOption, HasCorrect
    ],
) -> AbstractExerciseUseCase:
    """Provide the testing process use case."""
    return ExerciseProcessor(
        use_case_to_create=create_testing_task_use_case,
        use_case_to_check=check_testing_answer_use_case,
    )


def test_create_testing_task_with_command(
    testing_processor: ExecutableExercise[Testable],
) -> None:
    # Arrange
    command = CreateTaskCommand()

    # Act
    result = testing_processor.execute(command)

    # Assert
    assert result is not None
    assert hasattr(result, 'task')
    assert result.task is not None
    assert isinstance(result.task.question_text, str)
    assert isinstance(result.task.question_value, int)
    assert isinstance(result.task.options, list)


def test_check_testing_user_answer_with_command(
    testing_processor: ExecutableExercise[Testable],
) -> None:
    # Arrange
    command = CheckAnswerCommand()

    # Act
    result = testing_processor.execute(command)

    # Assert
    assert result is not None
    assert hasattr(result, 'is_correct')
