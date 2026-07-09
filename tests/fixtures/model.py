"""Domain model fixtures."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.factories.model import (
    create_testing_task,
    create_testing_task_dto,
    get_learnables,
)

if TYPE_CHECKING:
    from wse.application.protocols import TaskDtoProto
    from wse.domain.protocols import Testable, UniqueLearnable


@pytest.fixture
def learnables() -> tuple[UniqueLearnable, ...]:
    """Provide exercise task candidates."""
    return get_learnables()


@pytest.fixture
def testing_task(learnables: tuple[UniqueLearnable, ...]) -> Testable:
    """Provide a testing exercise task."""
    return create_testing_task(learnables)


@pytest.fixture
def testing_task_dto(testing_task: Testable) -> TaskDtoProto[Testable]:
    """Provide the testing task."""
    return create_testing_task_dto(testing_task)
