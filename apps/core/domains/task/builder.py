"""Exercise phase (definition / mean / random) orderer."""

from contracts.entity.domain.exercise import fields
from contracts.enums import DisplayOrder
from contracts.schemas.domain.exercise.flow import PresentationTask
from interfaces.protocols.domain.exercise import (
    CandidateProtocol,
    PresentationTaskProtocol,
)

from ..exercise.protocol import HasPhases
from .abstract import AbstractTaskBuilder

QUESTION_INDEX = 0
ANSWER_INDEX = 1


class PresentationTaskBuilder(
    AbstractTaskBuilder[
        fields.HasTaskItem[CandidateProtocol],
        HasPhases,
        PresentationTaskProtocol,
    ],
):
    """Presentation task builder."""

    def build(
        self,
        case: fields.HasTaskItem[CandidateProtocol],
        conf: HasPhases,
    ) -> PresentationTaskProtocol:
        """Build presentation task."""
        option = case.item

        return PresentationTask(
            question_text=self._get_question(option, conf.phases),
            answer_text=self._get_answer(option, conf.phases),
            progress_value=option.progress_value,
        )

    def _get_question(
        self,
        candidate: CandidateProtocol,
        phases: list[DisplayOrder],
    ) -> str:
        """Get question text by display case phase order."""
        return getattr(candidate, phases[QUESTION_INDEX])  # type: ignore[no-any-return]

    def _get_answer(
        self,
        candidate: CandidateProtocol,
        phases: list[DisplayOrder],
    ) -> str:
        """Get answer text by display case phase order."""
        return getattr(candidate, phases[ANSWER_INDEX])  # type: ignore[no-any-return]
