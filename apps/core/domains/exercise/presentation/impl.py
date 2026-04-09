"""Domain logic for selecting items for presentation cases."""

from random import choice

from ..abstract import AbstractConfigurableCandidatesExerciseDomain
from ..deps.protocol import SelectorProtocol
from ..protocol import (
    Candidate,
    Candidates,
    HasDisplayOrder,
)
from .dto import PresentationDomainResult
from .protocol import PresentationCreateResultProtocol

__all__ = ('PresentationDomain',)


class PresentationDomain(
    AbstractConfigurableCandidatesExerciseDomain[
        HasDisplayOrder,
        PresentationCreateResultProtocol[Candidate],
    ],
):
    """Presentation exercise case domain."""

    def __init__(
        self,
        selector: SelectorProtocol[HasDisplayOrder],
    ) -> None:
        """Configure the domain."""
        self._selector = selector

    def execute(
        self,
        candidates: Candidates,
        conf: HasDisplayOrder,
    ) -> PresentationCreateResultProtocol[Candidate]:
        """Get presentation exercise case data."""
        selected_candidates = self._selector.select(candidates, conf)
        option = choice(selected_candidates)

        return PresentationDomainResult(
            option=option,
        )
