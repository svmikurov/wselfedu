"""In memory repository."""

from __future__ import annotations

from typing import TYPE_CHECKING

from wse.config import DATA_PATH
from wse.domain.entities import ItemStudy
from wse.infrastructure.abstract import AbstractRepository
from wse.utils.io import load_json

if TYPE_CHECKING:
    from pathlib import Path

    from wse.domain.protocols import UniqueLearnable

CANDIDATES_PATH = DATA_PATH / 'candidates.json'


class InMemoryCandidatesRepository(AbstractRepository):
    """Temporary repository for candidates."""

    def __init__(self) -> None:
        self._candidates = self._get_candidates()

    def list(self) -> list[UniqueLearnable]:
        """Get candidates."""
        return list(self._candidates)

    @staticmethod
    def _get_candidates(path: Path = CANDIDATES_PATH) -> set[UniqueLearnable]:
        """Build candidate instances from JSON data."""
        items = load_json(path)
        if not isinstance(items, list):
            raise ValueError(f'Expected `list`, got {type(items).__name__}')

        candidates: set[UniqueLearnable] = set()
        for data in items:
            if not isinstance(data, dict):
                raise ValueError(
                    f'Expected `dict` per item, got {type(data).__name__}'
                )
            candidates.add(ItemStudy(**data))

        return candidates
