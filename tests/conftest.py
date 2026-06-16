"""Pytest configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from wse.config import DATA_PATH
from wse.domain.entities import StudyItem
from wse.utils.io import load_json

if TYPE_CHECKING:
    from wse.domain.protocols import UniqueLearnable

    from .types import LearnableTypedData


@pytest.fixture
def task_candidates() -> list[UniqueLearnable]:
    """Provide exercise task candidates."""
    items: list[LearnableTypedData] = load_json(DATA_PATH / 'candidates.json')
    return [StudyItem(**data) for data in items]
