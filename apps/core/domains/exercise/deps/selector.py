"""Domain resource selector."""

from apps.core.exceptions import info
from contracts.aliases import CandidatesAlias
from contracts.entity.domain.exercise.fields import HasItemCount

from ..deps.abstract import AbstractSelector


class CandidatesSelector(
    AbstractSelector[HasItemCount],
):
    """Exercise candidates selector."""

    MIN_CANDIDATES_COUNT = 2

    def select(
        self,
        candidates: CandidatesAlias,
        conf: HasItemCount,
    ) -> CandidatesAlias:
        """Select translation for exercise."""
        if len(candidates) < self.MIN_CANDIDATES_COUNT:
            raise info.NoExerciseItemsException(
                f'Expected {self.MIN_CANDIDATES_COUNT} or more candidates, '
                f'but got {len(candidates)}'
            )
        return candidates.order_by('id')[: conf.item_count]
