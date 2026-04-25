"""Protocol for exercise domain dependencies."""

from typing import Protocol, TypeVar

from interfaces.aliases import CandidatesAlias

Conf_contra = TypeVar('Conf_contra', contravariant=True)


class SelectorProtocol(Protocol[Conf_contra]):
    """Protocol for exercise data selector interface."""

    def select(
        self,
        candidates: CandidatesAlias,
        conf: Conf_contra,
    ) -> CandidatesAlias:
        """Select data for exercise."""
