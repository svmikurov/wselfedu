"""Word study service."""

from random import choice

from .. import types
from .abc import WordStudyDomainABC


class WordStudyDomain(WordStudyDomainABC):
    """Word study case service."""

    def create(self, params: types.WordStudyParams) -> types.WordStudyCase:
        """Create Word study case.

        Creates Word study case from selected **translation IDs**.

        Parameters
        ----------
        params : `WordStudyParams`
            Create case parameters.

        Returns
        -------
        `WordStudyCase`
            Exercise case to fetch word data.
            Not contains words to study.

        """
        return types.WordStudyCase(
            translation_id=self._get_random_id(params.translation_ids)
        )

    def _get_random_id(self, ids: list[int]) -> int:
        """Get random id."""
        return choice(ids)
