"""Protocol for DTO builder."""

from typing import Protocol, TypeVar

DTO_contra = TypeVar('DTO_contra', contravariant=True)
DTO_co = TypeVar('DTO_co', covariant=True)
Spec_contra = TypeVar('Spec_contra', contravariant=True)


class DtoBuilderProtocol(Protocol[DTO_contra, DTO_co]):
    """Protocol for a DTO builder interface."""

    def build(
        self,
        data: DTO_contra,
    ) -> DTO_co:
        """Build the DTO."""


class SpecDtoBuilderProtocol(
    Protocol[
        DTO_contra,
        Spec_contra,
        DTO_co,
    ]
):
    """Protocol for a DTO builder that follows the specification."""

    def build(
        self,
        data: DTO_contra,
        spec: Spec_contra,
    ) -> DTO_co:
        """Build a DTO according to the specification."""
