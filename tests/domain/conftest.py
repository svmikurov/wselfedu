"""Domain layer pytest configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from wse.domain.values import (
    TaskCreating,
    TestingParameters,
)

if TYPE_CHECKING:
    from wse.domain.protocols import TestingCreatableSpec, UniqueLearnable


@pytest.fixture
def create_testing_spec(
    learnables: tuple[UniqueLearnable, ...],
) -> TestingCreatableSpec:
    """Provide a create testing task specification."""
    return TaskCreating(
        learnables=learnables,
        params=TestingParameters(
            option_count=3,
        ),
    )
