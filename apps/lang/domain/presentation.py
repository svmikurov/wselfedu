"""Word study presentation domain logic.

This over-engineering demonstrates clean architecture for educational
purposes, separating domain logic even when simple.
"""

from random import choice

from .. import types
from .abc import WordStudyDomainABC


class WordStudyDomain(WordStudyDomainABC):
    """Word study case service."""

    def create(self, params: types.CaseCandidates) -> types.WordStudyCase:
        """Create Word study case.

        Creates Word study case from selected **translation IDs**.

        Parameters
        ----------
        params : `WordStudyParameters`
            Create presentation case parameters.

        Returns
        -------
        `WordStudyCase`
            Exercise case to fetch word data.
            Not contains words to study.

        """
        return types.WordStudyCase(
            translation_id=choice(params.translation_ids)
        )
