"""Domain logic for selecting items for presentation cases."""

from __future__ import annotations

from random import choice
from typing import TYPE_CHECKING

from apps.core.exceptions import info

from .abstract import AbstractCreateExerciseDomain
from .presentation_dto import PresentationCase, PresentationMeta
from .types import Settings

type Result = tuple[PresentationCase, PresentationMeta]

if TYPE_CHECKING:
    from .enums import DisplayOrder
    from .types import Candidate, Candidates, ExerciseConfig, Settings


__all__ = [
    'PresentationDomain',
]


class PresentationDomain(AbstractCreateExerciseDomain[Settings, Result]):
    """Presentation exercise domain logic."""

    MIN_CANDIDATES_COUNT = 2

    def __init__(self, config: ExerciseConfig) -> None:
        """Configure the domain."""
        self._item_count: int = config.item_count

    def execute(self, candidates: Candidates, settings: Settings) -> Result:
        """Get presentation exercise case data."""
        if len(candidates) < self.MIN_CANDIDATES_COUNT:
            raise info.NoExerciseItemsException

        limited_candidates = self._get_limited(candidates)
        candidate = choice(limited_candidates)

        case = self._build_case(candidate, settings.display_order)
        meta = self._build_meta(candidate)
        return case, meta

    def _get_limited(self, candidates: Candidates) -> Candidates:
        """Limit candidates for exercise."""
        # Temporary returns first database query items
        # TODO: Implement candidates limit order
        # after additional processing by service
        return candidates.order_by('id')[: self._item_count]

    @staticmethod
    def _build_case(
        candidate: Candidate, order: DisplayOrder
    ) -> PresentationCase:
        """Build exercise case DTO to rendering."""
        question, answer = order.get_display_phases()
        return PresentationCase(
            question_text=getattr(candidate, question),
            answer_text=getattr(candidate, answer),
            progress=candidate.progress,
        )

    @staticmethod
    def _build_meta(candidate: Candidate) -> PresentationMeta:
        """Build exercise case metadata DTO for internal tracking."""
        return PresentationMeta(pk=candidate.pk)
