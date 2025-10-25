"""Word study service."""

from random import choice

from ..types import WordStudyCase, WordStudyParams
from .abc import WordStudyServiceABC


class WordStudyService(WordStudyServiceABC):
    """Word study service to create task case."""

    def create(self, params: WordStudyParams) -> WordStudyCase:
        """Create word study task case."""
        return WordStudyCase(definition_id=self._get_random_id(params.ids))

    def _get_random_id(self, ids: list[int]) -> int:
        """Get random id."""
        return choice(ids)
