"""Create presentation domain service tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wse.application.abstract import AbstractCreateTaskUseCase
    from wse.domain.protocols import (
        Learnable,
        Testable,
    )


def test_create_task_use_case(
    create_testing_task_use_case: AbstractCreateTaskUseCase[Testable],
) -> None:
    # Act
    task = create_testing_task_use_case.execute()

    # Assert
    # - that task created
    assert task is not None
    # - that task has attributes
    assert hasattr(task, 'question_text')
    assert hasattr(task, 'question_value')
    assert hasattr(task, 'options')
    # - that task attributes has type
    assert isinstance(task.question_text, str)
    assert isinstance(task.question_value, int)
    assert isinstance(task.options, list)
    # - that option has attributes
    option = task.options[0]
    assert isinstance(option.value, int)
    assert isinstance(option.text, str)


def test_option_value_is_correct_answer_for_question(
    create_testing_task_use_case: AbstractCreateTaskUseCase[Testable],
    candidates: list[Learnable],
) -> None:
    # Act
    task = create_testing_task_use_case.execute()

    # Assert
    studied_item = next(
        item for item in candidates if item.define == task.question_text
    )
    correct_option = task.options[task.question_value - 1]
    assert correct_option.text == studied_item.explain
