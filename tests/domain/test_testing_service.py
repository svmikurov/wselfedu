"""Testing exercise domain service tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from wse.domain import services

if TYPE_CHECKING:
    from wse.domain.protocols import (
        Creatable,
        Testable,
        TestingCreatableSpec,
    )


@pytest.fixture
def create_testing_service() -> Creatable[TestingCreatableSpec, Testable]:
    """Provide a create testing service."""
    return services.CreateTestingService()


def test_create_testing_task(
    create_testing_service: Creatable[TestingCreatableSpec, Testable],
    create_testing_spec: TestingCreatableSpec,
) -> None:
    # Act
    task = create_testing_service.create(create_testing_spec)

    # Assert
    assert hasattr(task, 'question_text')
    assert isinstance(task.question_text, str)
    assert hasattr(task, 'options')
    assert isinstance(task.options, tuple)

    option = task.options[0]
    assert hasattr(option, 'option_value')
    assert isinstance(option.option_value, int)
    assert hasattr(option, 'option_text')
    assert isinstance(option.option_text, str)
