"""Domain logic for selecting items for presentation cases."""

from random import choice

from contracts import enums
from contracts.entity.domain.exercise.flow import (
    PresentationDomainResultProtocol,
)
from interfaces.protocols.domain.exercise import (
    CandidatesT,
    ExerciseConfigProtocol,
)
from interfaces.schemas.domain.exercise import (
    PresentationExerciseDomainResult,
)

from ..abstract import AbstractConfigurableCandidatesExerciseDomain
from ..deps.protocol import SelectorProtocol

__all__ = ('PresentationDomain',)


class PresentationDomain(
    AbstractConfigurableCandidatesExerciseDomain[
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

        return PresentationExerciseDomainResult(  # type: ignore
            status=enums.ExerciseStatus.NEW_TASK,
            exercise_kind=enums.ExerciseKind.PRESENTATION,
            item=option,  # type: ignore
        )
