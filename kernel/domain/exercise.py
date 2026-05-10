"""Exercise domain."""

from apps.core.exceptions import info
from interfaces.protocols.domain.exercise import CandidatesT
from ports.abstract.domain.exercise import AbstractSelector
from ports.contract.entity.domain.exercise.fields import HasItemCount

# =================================================
# Exercise domain resource selector
# =================================================


class CandidatesSelector(
    AbstractSelector[HasItemCount],
):
    """Exercise candidates selector."""

    MIN_CANDIDATES_COUNT = 2

    def select(
        self,
        candidates: CandidatesT,
        conf: HasItemCount,
    ) -> CandidatesT:
        """Select translation for exercise."""
        if len(candidates) < self.MIN_CANDIDATES_COUNT:
            raise info.NoExerciseItemsException(
                f'Expected {self.MIN_CANDIDATES_COUNT} or more candidates, '
                f'but got {len(candidates)}'
            )
        return candidates[: conf.item_count]
