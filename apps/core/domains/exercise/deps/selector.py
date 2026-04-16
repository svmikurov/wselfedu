"""Domain resource selector."""

from apps.core.contracts.business import HasItemCount
from apps.core.exceptions import info

from ..deps.abstract import AbstractSelector
from ..protocol import Candidates


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
            raise info.NoExerciseItemsException(
                f'Expected {self.MIN_CANDIDATES_COUNT} or more candidates, '
                f'but got {len(candidates)}'
            )
        return candidates.order_by('id')[: conf.item_count]
