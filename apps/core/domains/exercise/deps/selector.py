"""Domain resource selector."""

from apps.core.exceptions import info
from contracts.entity.domain.exercise.fields import HasItemCount
from interfaces.protocols.domain.exercise import CandidatesProtocol

from ..deps.abstract import AbstractSelector


class CandidatesSelector(
    AbstractSelector[HasItemCount],
):
    """Exercise candidates selector."""

    MIN_CANDIDATES_COUNT = 2

    def select(
        self,
        candidates: CandidatesProtocol,
        conf: HasItemCount,
    ) -> CandidatesProtocol:
        """Select translation for exercise."""
        if len(candidates) < self.MIN_CANDIDATES_COUNT:
            raise info.NoExerciseItemsException(
                f'Expected {self.MIN_CANDIDATES_COUNT} or more candidates, '
                f'but got {len(candidates)}'
            )
        return candidates[: conf.item_count]
