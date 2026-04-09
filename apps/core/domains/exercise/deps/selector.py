"""Domain resource selector."""

from apps.core.exceptions import info

from ..deps.abstract import AbstractSelector
from ..protocol import Candidates, HasItemCount


class CandidatesSelector(
    AbstractSelector[HasItemCount],
):
    """Exercise candidates selector."""

    MIN_CANDIDATES_COUNT = 2

    def select(
        self,
        candidates: Candidates,
        conf: HasItemCount,
    ) -> Candidates:
        """Select translation for exercise."""
        if len(candidates) < self.MIN_CANDIDATES_COUNT:
            raise info.NoExerciseItemsException
        return candidates.order_by('id')[: conf.item_count]
