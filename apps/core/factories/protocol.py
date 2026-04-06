"""Protocol for factories."""

from abc import abstractmethod
from typing import Protocol, TypeVar

Case_contra = TypeVar('Case_contra', contravariant=True)
Conf_contra = TypeVar('Conf_contra', contravariant=True)
Result_cov = TypeVar('Result_cov', covariant=True)

LockupCommand = TypeVar('LockupCommand')
LockupConditions = TypeVar('LockupConditions')


class CaseFactoryProtocol(Protocol[Conf_contra, Case_contra, Result_cov]):
    """Protocol for exercise case DTO factory."""

    @abstractmethod
    def build(self, conf: Conf_contra, case: Case_contra) -> Result_cov:
        """Build exercise DTO."""
