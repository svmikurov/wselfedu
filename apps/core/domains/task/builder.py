"""Exercise phase (definition / mean / random) orderer."""

from contracts.entity.domain.exercise import fields
from contracts.enums import DisplayOrder, ExerciseStatus
from contracts.schemas.domain.exercise.flow import PresentationTask
from interfaces.protocols.domain.exercise import (
    Candidate,
    PresentationTaskProtocol,
)

from ..exercise.protocol import HasPhases
from .abstract import AbstractTaskBuilder

QUESTION_INDEX = 0
ANSWER_INDEX = 1


class PresentationTaskBuilder(
    AbstractTaskBuilder[
        fields.HasExerciseDomainOption[Candidate],
        HasPhases,
        PresentationTaskProtocol,
    ],
):
    """Presentation task builder."""

    def build(
        self,
        case: fields.HasExerciseDomainOption[Candidate],
        conf: HasPhases,
    ) -> PresentationTaskProtocol:
        """Build presentation task."""
        option = case.option

        return PresentationTask(
            status=ExerciseStatus.NEW_TASK,
            question_text=self._get_question(option, conf.phases),
            answer_text=self._get_answer(option, conf.phases),
            progress_value=option.progress_value,
        )

    def _get_question(
        self,
        candidate: Candidate,
        phases: list[DisplayOrder],
    ) -> str:
        """Get question text by display case phase order."""
        return getattr(candidate, phases[QUESTION_INDEX])  # type: ignore[no-any-return]

    def _get_answer(
        self,
        candidate: Candidate,
        phases: list[DisplayOrder],
    ) -> str:
        """Get answer text by display case phase order."""
        return getattr(candidate, phases[ANSWER_INDEX])  # type: ignore[no-any-return]
