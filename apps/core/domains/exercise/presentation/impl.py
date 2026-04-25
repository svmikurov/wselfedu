"""Domain logic for selecting items for presentation cases."""

from random import choice

from interfaces.aliases import CandidatesAlias

from ..abstract import AbstractConfigurableCandidatesExerciseDomain
from ..deps.protocol import SelectorProtocol
from ..protocol import ExerciseConfigProtocol
from .dto import PresentationDomainResult
from .protocol import PresentationCreateResultProtocol

__all__ = ('PresentationDomain',)


class PresentationDomain(
    AbstractConfigurableCandidatesExerciseDomain[
        ExerciseConfigProtocol,
        PresentationCreateResultProtocol,
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
        candidates: CandidatesAlias,
        conf: ExerciseConfigProtocol,
    ) -> PresentationCreateResultProtocol:
        """Get presentation exercise case data."""
        selected_candidates = self._selector.select(candidates, conf)
        option = choice(selected_candidates)

        return PresentationDomainResult(
            option=option,
        )
