"""Domain model fixtures."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.factories.model import create_testing_task, get_learnables

if TYPE_CHECKING:
    from wse.domain.protocols import Testable, UniqueLearnable


@pytest.fixture
def learnables() -> tuple[UniqueLearnable, ...]:
    """Provide exercise task candidates."""
    return get_learnables()


@pytest.fixture
def testing_task(learnables: tuple[UniqueLearnable, ...]) -> Testable:
    """Provide a testing exercise task."""
    return create_testing_task(learnables)
