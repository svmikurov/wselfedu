"""Testing exercise domain service tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.factories.model import TESTING_TASK_OPTION_COUNT, get_learnables
from wse.domain import exceptions, services, values
from wse.domain.constraints import TaskConstraints

if TYPE_CHECKING:
    from wse.domain.protocols import HasOptionCount, Testable, UniqueLearnable


def create_testing_task_via_service(
    learnables: tuple[UniqueLearnable, ...] | None = None,
    params: HasOptionCount | None = None,
) -> Testable:
    """Create a testing task uses service by exercise parameters."""
    testing_spec_create = values.TaskCreating(
        learnables=learnables or get_learnables(),
        params=params
        or values.TestingParameters(
            option_count=TESTING_TASK_OPTION_COUNT,
        ),
    )
    return services.CreateTestingService().create(testing_spec_create)


@pytest.fixture
def task(
    learnables: tuple[UniqueLearnable, ...],
) -> Testable:
    """Provide task created by domain service."""
    return create_testing_task_via_service(learnables)


def test_task_contains_attributes(task: Testable) -> None:
    # Assert
    assert hasattr(task, 'question_text')
    assert isinstance(task.question_text, str)
    assert task.question_text.strip(), 'Question text should not be empty'

    assert hasattr(task, 'options')
    assert isinstance(task.options, tuple)
    assert len(task.options) > 0

    for option in task.options:
        assert hasattr(option, 'option_value')
        assert isinstance(option.option_value, int)
        assert hasattr(option, 'option_text')
        assert isinstance(option.option_text, str)
        assert option.option_text.strip(), 'Option text should not be empty'


@pytest.mark.parametrize(
    'option_count',
    [TaskConstraints.MIN_OPTIONS, TaskConstraints.MAX_OPTIONS],
    ids=['min option count', 'max option count'],
)
def test_testing_task_contains_option_count(option_count: int) -> None:
    # Act
    testing_task = create_testing_task_via_service(
        params=values.TestingParameters(option_count=option_count)
    )

    # Assert
    assert len(testing_task.options) == option_count


@pytest.mark.parametrize(
    'option_count, expected_exception',
    [
        (0, exceptions.InvalidOptionCountError),
        (100, exceptions.InvalidOptionCountError),
    ],
    ids=['zero option count', 'option count more than learnable count'],
)
def test_exception_raises_when_incorrect_option_count(
    option_count: int,
    expected_exception: type[Exception],
) -> None:
    # Act & Assert
    with pytest.raises(expected_exception):
        create_testing_task_via_service(
            params=values.TestingParameters(option_count=option_count)
        )


def test_task_options_are_unique(task: Testable) -> None:
    # Arrange
    option_values = [opt.option_value for opt in task.options]
    option_texts = [opt.option_text for opt in task.options]

    # Assert
    assert len(set(option_values)) == len(option_values), (
        'Option values must be unique'
    )
    assert len(set(option_texts)) == len(option_texts), (
        'Option texts must be unique'
    )
