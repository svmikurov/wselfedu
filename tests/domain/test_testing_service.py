"""Testing exercise domain service tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

from wse.domain import services, values

if TYPE_CHECKING:
    from wse.domain.protocols import UniqueLearnable


def test_create_testing_task(
    task_candidates: list[UniqueLearnable],
) -> None:
    # Act
    task = services.create_testing_task(task_candidates)

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


def test_check_correct_user_answer(
    task_candidates: list[UniqueLearnable],
) -> None:
    # Arrange
    task = services.create_testing_task(task_candidates)
    correct_answer = task.question_value
    answer_spec = values.AnswerChecking(
        question_value=correct_answer,
        answer_value=correct_answer,
    )

    # Act
    checking_result = services.check_testing_answer(answer_spec)

    # Assert
    assert checking_result.is_correct is True


def test_check_wrong_user_answer(
    task_candidates: list[UniqueLearnable],
) -> None:
    # Arrange
    task = services.create_testing_task(task_candidates)
    correct_answer = task.question_value
    wrong_answer = (
        correct_answer + 1 if correct_answer == 1 else correct_answer - 1
    )
    answer_spec = values.AnswerChecking(
        question_value=correct_answer,
        answer_value=wrong_answer,
    )

    # Act
    checking_result = services.check_testing_answer(answer_spec)

    # Assert
    assert checking_result.is_correct is False
