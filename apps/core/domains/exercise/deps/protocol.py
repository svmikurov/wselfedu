"""Protocol for exercise domain dependencies."""

from typing import Protocol, TypeVar

from contracts import aliases
from interfaces.schemas.domain.exercise import TaskItem

Conf_contra = TypeVar('Conf_contra', contravariant=True)


class SelectorProtocol(Protocol[Conf_contra]):
    """Protocol for exercise data selector interface."""

    def select(
        self,
        candidates: aliases.CandidatesAlias,
        conf: Conf_contra,
    ) -> list[TaskItem]:
        """Select data for exercise."""
