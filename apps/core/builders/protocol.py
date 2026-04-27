"""Protocol for DTO builder."""

from abc import abstractmethod
from typing import Protocol, TypeVar

from interfaces.entity.domain.exercise.fields import HasExerciseStatus

Candidate_contra = TypeVar('Candidate_contra', contravariant=True)
Case_co = TypeVar('Case_co', covariant=True)
Case_contra = TypeVar('Case_contra', contravariant=True)

DomainT_contra = TypeVar('DomainT_contra', contravariant=True)
SpecT_contra = TypeVar('SpecT_contra', contravariant=True)
Task_co = TypeVar('Task_co', bound=HasExerciseStatus, covariant=True)


class DtoBuilderProtocol(Protocol[Candidate_contra, Case_co]):
    """Protocol for exercise case DTO builder."""

    @abstractmethod
    def build(
        self,
        data: Candidate_contra,
    ) -> Case_co:
        """Build exercise case DTO."""


class SpecDtoBuilderProtocol(
    Protocol[
        Case_contra,
        SpecT_contra,
        Task_co,
    ]
):
    """Protocol for DTO builder by specification."""

    def build(
        self,
        data: Case_contra,
        spec: SpecT_contra,
    ) -> Task_co:
        """Build exercise task DTO."""
