"""Protocols for exercise domain interface."""

from typing import Protocol, TypeVar

from interfaces.protocols.domain.exercise import CandidatesT

ExerciseConfig_contra = TypeVar('ExerciseConfig_contra', contravariant=True)
Option_co = TypeVar('Option_co', covariant=True)


class CreateTaskDomainProtocol(
    Protocol[
        ExerciseConfig_contra,
        Option_co,
    ],
):
    """Protocol for create exercise task domain interface."""

    def execute(
        self,
        candidates: CandidatesT,
        conf: ExerciseConfig_contra,
    ) -> Option_co:
        """Create exercise case."""
