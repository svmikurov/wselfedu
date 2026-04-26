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


class CaseBuilderProtocol(Protocol[Candidate_contra, Case_co]):
    """Protocol for exercise case DTO builder."""

    @abstractmethod
    def build(
        self,
        option: Candidate_contra,
    ) -> Case_co:
        """Build exercise case DTO."""


class ExerciseTaskBuilderProtocol(
    Protocol[
        Case_contra,
        SpecT_contra,
        Task_co,
    ]
):
    """Protocol for exercise task DTO builder interface."""

    def build(
        self,
        case: Case_contra,
        spec: SpecT_contra,
    ) -> Task_co:
        """Build exercise task DTO."""
