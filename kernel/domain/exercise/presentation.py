"""Domain logic for selecting items for presentation cases."""

from random import choice

from ports.abstract.domain.exercise import AbstractCandidatesExerciseDomain
from ports.contract import enums
from ports.contract.infra.domain.selector import SelectorProtocol
from ports.interfaces.protocols.domain.exercise import (
    CandidatesT,
    ExerciseConfigProtocol,
    PresentationDomainResultProtocol,
)
from ports.interfaces.schemas.domain.exercise.exercise import (
    PresentationTaskDomainResult,
)

__all__ = ('PresentationDomain',)


class PresentationDomain(
    AbstractCandidatesExerciseDomain[
        ExerciseConfigProtocol,
        PresentationDomainResultProtocol,
    ],
):
    """Presentation exercise case domain."""

    def __init__(
        self,
        selector: SelectorProtocol[ExerciseConfigProtocol],
    ) -> None:
        """Configure the domain."""
        self._selector = selector

    def execute(
        self,
        candidates: CandidatesT,
        conf: ExerciseConfigProtocol,
    ) -> PresentationDomainResultProtocol:
        """Get presentation exercise case data."""
        selected_candidates = self._selector.select(candidates, conf)
        option = choice(selected_candidates)

        return PresentationTaskDomainResult(
            status=enums.ExerciseStatus.NEW_TASK,
            exercise_kind=enums.ExerciseKind.PRESENTATION,
            item=option,  # type: ignore
        )
