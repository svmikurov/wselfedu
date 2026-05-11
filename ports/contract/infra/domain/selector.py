"""Protocol for exercise domain dependencies."""

from typing import Protocol, TypeVar

from ports.interfaces.protocols.domain.exercise import CandidatesT

Conf_contra = TypeVar('Conf_contra', contravariant=True)


class SelectorProtocol(Protocol[Conf_contra]):
    """Protocol for exercise data selector interface."""

    def select(
        self,
        candidates: CandidatesT,
        conf: Conf_contra,
    ) -> CandidatesT:
        """Select data for exercise."""
