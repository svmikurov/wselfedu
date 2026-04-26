"""Protocol for exercise domain dependencies."""

from typing import Protocol, TypeVar

from interfaces import aliases

Conf_contra = TypeVar('Conf_contra', contravariant=True)


class SelectorProtocol(Protocol[Conf_contra]):
    """Protocol for exercise data selector interface."""

    def select(
        self,
        candidates: aliases.CandidatesAlias,
        conf: Conf_contra,
    ) -> aliases.CandidatesAlias:
        """Select data for exercise."""
