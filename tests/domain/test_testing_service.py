"""Testing exercise domain service tests."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeAlias

import pytest

from wse.domain import services, values

if TYPE_CHECKING:
    from wse.domain.protocols import (
        AnswerCheckable,
        CheckableOption,
        ExerciseCreatable,
        HasIsCorrect,
        HasLearnables,
        Testable,
        UniqueLearnable,
    )

    SpecificationT: TypeAlias = HasLearnables[list[UniqueLearnable]]
    CreateServiceT: TypeAlias = ExerciseCreatable[SpecificationT, Testable]
    CheckServiceT: TypeAlias = AnswerCheckable[CheckableOption, HasIsCorrect]


@pytest.fixture
def create_testing_service() -> CreateServiceT:
    """Provide a create testing service."""
    return services.CreateTestingService()


@pytest.fixture
def check_answer_service() -> CheckServiceT:
    """Provide a check testing  answer service."""
    return services.CheckTestingService()


@pytest.fixture
def testing_task(
    create_testing_service: CreateServiceT,
    create_testing_spec: SpecificationT,
) -> Testable:
    """Provide a testing task."""
    return create_testing_service.create(create_testing_spec)


def test_create_testing_task(testing_task: Testable) -> None:
    # Assert
    assert hasattr(testing_task, 'question_text')
    assert isinstance(testing_task.question_text, str)
    assert hasattr(testing_task, 'options')
    assert isinstance(testing_task.options, list)

    option = testing_task.options[0]
    assert hasattr(option, 'option_value')
    assert isinstance(option.option_value, int)
    assert hasattr(option, 'option_text')
    assert isinstance(option.option_text, str)


def test_check_correct_user_answer(
    testing_task: Testable,
    check_answer_service: CheckServiceT,
) -> None:
    # Arrange
    correct_answer = testing_task.question_value
    answer_spec = values.AnswerChecking(
        question_value=correct_answer,
        answer_value=correct_answer,
    )

    # Act
    checking_result = check_answer_service.check(answer_spec)

    # Assert
    assert checking_result.is_correct is True


def test_check_wrong_user_answer(
    testing_task: Testable,
    check_answer_service: CheckServiceT,
) -> None:
    # Arrange
    correct_answer = testing_task.question_value
    wrong_answer = (
        correct_answer - 1 if correct_answer > 1 else correct_answer + 1
    )
    answer_spec = values.AnswerChecking(
        question_value=correct_answer,
        answer_value=wrong_answer,
    )

    # Act
    checking_result = check_answer_service.check(answer_spec)

    # Assert
    assert checking_result.is_correct is False
