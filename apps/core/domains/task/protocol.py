"""Protocol for exercise domain dependencies."""

from typing import Protocol, TypeVar

from utils.audit.protocol import Auditable

Conf_contra = TypeVar('Conf_contra', contravariant=True)
Case_contra = TypeVar('Case_contra', contravariant=True)
Task_cov = TypeVar('Task_cov', covariant=True)


class TaskBuilderProtocol(
    Auditable,
    Protocol[Case_contra, Conf_contra, Task_cov],
):
    """Protocol cor Exercise task builder interface."""

    def build(
        self,
        domain: Case_contra,
        conf: Conf_contra,
    ) -> Task_cov:
        """Build exercise task."""
