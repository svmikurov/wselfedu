"""Exercise phase (definition / mean / random) orderer."""

from interfaces.enums import DisplayOrder, ExerciseStatus
from interfaces.protocols.domain.exercise import Candidate
from interfaces.schemas.domain.exercise.presentation import PresentationTask

from ..exercise.presentation.protocol import PresentationTaskProtocol
from ..exercise.protocol import HasOption, HasPhases
from .abstract import AbstractTaskBuilder

QUESTION_INDEX = 0
ANSWER_INDEX = 1


class PresentationTaskBuilder(
    AbstractTaskBuilder[
        HasOption[Candidate],
        HasPhases,
        PresentationTaskProtocol,
    ],
):
    """Presentation task builder."""

    def build(
        self,
        case: HasOption[Candidate],
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
