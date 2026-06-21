"""Pytest configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from wse.config import DATA_PATH
from wse.di.application import ApplicationContainer
from wse.domain.entities import StudyItem
from wse.domain.values import (
    Option,
    TaskCreating,
    Testing,
    TestingParameters,
)
from wse.utils.io import load_json

if TYPE_CHECKING:
    from wse.domain.protocols import HasLearnables, Testable, UniqueLearnable

    from .types import LearnableTypedData


@pytest.fixture
def learnables() -> tuple[UniqueLearnable, ...]:
    """Provide exercise task candidates."""
    items: list[LearnableTypedData] = load_json(DATA_PATH / 'candidates.json')
    return tuple(StudyItem(**data) for data in items)


@pytest.fixture
def create_testing_spec(
    learnables: tuple[UniqueLearnable, ...],
) -> HasLearnables[tuple[UniqueLearnable, ...]]:
    """Provide a create testing task specification."""
    return TaskCreating(
        learnables=learnables,
        params=TestingParameters(
            option_count=3,
        ),
    )


@pytest.fixture
def testing_task(learnables: tuple[UniqueLearnable, ...]) -> Testable:
    """Provide a testing exercise task."""
    option_count = 3
    selected_index = 0
    user_value = selected_index + 1

    question_item = learnables[selected_index]

    return Testing(
        question_text=question_item.define,
        question_value=user_value,
        options=tuple(
            Option(option_value=value, option_text=item.explain)
            for value, item in enumerate(learnables[:option_count], start=1)
        ),
    )


@pytest.fixture
def container() -> ApplicationContainer:
    """Provide a application DI container."""
    return ApplicationContainer()
