"""In memory repository."""

from __future__ import annotations

from typing import TYPE_CHECKING

from wse.domain.entities import ItemStudy
from wse.infrastructure.abstract import AbstractRepository

if TYPE_CHECKING:
    from wse.domain.protocols import Learnable


CANDIDATES: set[Learnable] = {
    ItemStudy(1, 'definition-1', 'explanation-1'),
    ItemStudy(2, 'definition-2', 'explanation-2'),
    ItemStudy(3, 'definition-3', 'explanation-3'),
    ItemStudy(4, 'definition-4', 'explanation-4'),
    ItemStudy(5, 'definition-5', 'explanation-5'),
}


class InMemoryCandidatesRepository(AbstractRepository):
    """Temporary repository for candidates."""

    def __init__(self) -> None:
        self._candidates = CANDIDATES

    def list(self) -> list[Learnable]:
        """Get candidates."""
        return list(self._candidates)
