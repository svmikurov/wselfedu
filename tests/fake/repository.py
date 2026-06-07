"""Fake repository."""

from wse.domain.protocols import Learnable
from wse.infrastructure.abstract import AbstractRepository

from ..conftest import CANDIDATES


class FakeCandidatesRepository(AbstractRepository):
    def __init__(self) -> None:
        self._candidates = CANDIDATES

    def list(self) -> list[Learnable]:
        return list(self._candidates)
