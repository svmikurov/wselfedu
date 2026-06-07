"""Fake repository."""

from __future__ import annotations

from typing import TYPE_CHECKING

from wse.infrastructure.abstract import AbstractRepository

if TYPE_CHECKING:
    from wse.domain.protocols import UniqueLearnable


class FakeCandidatesRepository(AbstractRepository):
    def __init__(self, candidates: list[UniqueLearnable]) -> None:
        self._candidates = set(candidates)

    def list(self) -> list[UniqueLearnable]:
        return list(self._candidates)
