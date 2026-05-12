"""Protocol for DTO builder."""

from typing import Protocol, TypeVar

from utils.audit.protocol import Auditable

Case_contra = TypeVar('Case_contra', contravariant=True)
DTO_co = TypeVar('DTO_co', covariant=True)
Spec_contra = TypeVar('Spec_contra', contravariant=True)

Conf_contra = TypeVar('Conf_contra', contravariant=True)
Task_co = TypeVar('Task_co', covariant=True)


class DtoBuilderProtocol(Protocol[Case_contra, DTO_co]):
    """Protocol for a DTO builder interface."""

    def build(
        self,
        case: Case_contra,
    ) -> DTO_co:
        """Build the DTO."""


class SpecDtoBuilderProtocol(
    Protocol[
        Case_contra,
        Spec_contra,
        DTO_co,
    ]
):
    """Protocol for a DTO builder that follows the specification."""

    def build(
        self,
        case: Case_contra,
        spec: Spec_contra,
    ) -> DTO_co:
        """Build a DTO according to the specification."""


class TaskBuilderProtocol(
    Auditable,
    Protocol[Case_contra, Conf_contra, Task_co],
):
    """Protocol cor Exercise task builder interface."""

    def build(
        self,
        case: Case_contra,
        conf: Conf_contra,
    ) -> Task_co:
        """Build exercise task."""
