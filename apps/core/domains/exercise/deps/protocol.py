"""Protocol for exercise domain dependencies."""

from typing import Protocol, TypeVar

from ..protocol import Candidates

Conf_contra = TypeVar('Conf_contra', contravariant=True)


class SelectorProtocol(Protocol[Conf_contra]):
    """Protocol for exercise data selector interface."""

    def select(
        self,
        candidates: Candidates,
        conf: Conf_contra,
    ) -> Candidates:
        """Select data for exercise."""
