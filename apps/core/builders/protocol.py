"""Protocol for DTO builder."""

from abc import abstractmethod
from typing import Protocol, TypeVar

from interfaces.protocols.domain.exercise import HasExerciseStatus

Candidate_contra = TypeVar('Candidate_contra', contravariant=True)
Case_cov = TypeVar('Case_cov', covariant=True)

DomainT_contra = TypeVar('DomainT_contra', contravariant=True)
SpecT_contra = TypeVar('SpecT_contra', contravariant=True)
ResultT_co = TypeVar('ResultT_co', bound=HasExerciseStatus, covariant=True)


class CaseBuilderProtocol(Protocol[Candidate_contra, Case_cov]):
    """Protocol for exercise case DTO builder."""

    @abstractmethod
    def build(
        self,
        option: Candidate_contra,
    ) -> Case_cov:
        """Build exercise case DTO."""


class ExerciseTaskBuilderProtocol(
    Protocol[
        DomainT_contra,
        SpecT_contra,
        ResultT_co,
    ]
):
    """Protocol for exercise task DTO builder interface."""

    def build(
        self,
        domain: DomainT_contra,
        spec: SpecT_contra,
    ) -> ResultT_co:
        """Build exercise task DTO."""
