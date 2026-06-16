"""Testing exercise domain service tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

from wse.domain.services import create_testing_task

if TYPE_CHECKING:
    from wse.domain.protocols import UniqueLearnable


def test_create_testing_task(
    task_candidates: list[UniqueLearnable],
) -> None:
    # Act
    task = create_testing_task(task_candidates)

    # Assert
    assert hasattr(task, 'question_text')
    assert isinstance(task.question_text, str)
    assert hasattr(task, 'options')
    assert isinstance(task.options, list)

    option = task.options[0]
    assert hasattr(option, 'option_value')
    assert isinstance(option.option_value, int)
    assert hasattr(option, 'option_text')
    assert isinstance(option.option_text, str)
