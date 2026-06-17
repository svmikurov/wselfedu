"""Pytest configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from wse.config import DATA_PATH
from wse.domain.entities import StudyItem
from wse.domain.values import TaskCreating
from wse.utils.io import load_json

if TYPE_CHECKING:
    from wse.domain.protocols import HasLearnables, UniqueLearnable

    from .types import LearnableTypedData


@pytest.fixture
def learnables() -> list[UniqueLearnable]:
    """Provide exercise task candidates."""
    items: list[LearnableTypedData] = load_json(DATA_PATH / 'candidates.json')
    return [StudyItem(**data) for data in items]


@pytest.fixture
def create_testing_spec(
    learnables: list[UniqueLearnable],
) -> HasLearnables[list[UniqueLearnable]]:
    """Provide a create testing task specification."""
    return TaskCreating(learnables=learnables)
