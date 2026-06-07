"""Pytest configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

import pytest

from wse.domain.entities import ItemStudy

if TYPE_CHECKING:
    from wse.domain.protocols import UniqueLearnable


def get_pk() -> Callable[[], int]:
    """Provide an unique database identifier."""
    counter = 0

    def _get_nex() -> int:
        nonlocal counter
        counter += 1
        return counter

    return _get_nex


CANDIDATES: list[UniqueLearnable] = [
    ItemStudy(get_pk(), 'definition-1', 'explanation-1'),  # type: ignore
    ItemStudy(get_pk(), 'definition-2', 'explanation-2'),  # type: ignore
    ItemStudy(get_pk(), 'definition-3', 'explanation-3'),  # type: ignore
    ItemStudy(get_pk(), 'definition-4', 'explanation-4'),  # type: ignore
    ItemStudy(get_pk(), 'definition-5', 'explanation-5'),  # type: ignore
]


@pytest.fixture
def candidates() -> list[UniqueLearnable]:
    """Provide a candidates for exercise."""
    return CANDIDATES
