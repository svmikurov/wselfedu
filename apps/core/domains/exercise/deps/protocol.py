"""Protocol for exercise domain dependencies."""

from typing import Protocol, TypeVar

from interfaces.protocols.domain.exercise import CandidatesProtocol

Conf_contra = TypeVar('Conf_contra', contravariant=True)


class SelectorProtocol(Protocol[Conf_contra]):
    """Protocol for exercise data selector interface."""

    def select(
        self,
        candidates: CandidatesProtocol,
        conf: Conf_contra,
    ) -> CandidatesProtocol:
        """Select data for exercise."""
