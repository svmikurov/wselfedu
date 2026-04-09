"""Protocol for DTO builder."""

from abc import abstractmethod
from typing import Protocol, TypeVar

Conf_contra = TypeVar('Conf_contra', contravariant=True)
Candidate_contra = TypeVar('Candidate_contra', contravariant=True)
Case_cov = TypeVar('Case_cov', covariant=True)


class CaseBuilderProtocol(Protocol[Candidate_contra, Case_cov]):
    """Protocol for exercise case DTO builder."""

    @abstractmethod
    def build(
        self,
        option: Candidate_contra,
    ) -> Case_cov:
        """Build exercise case DTO."""
