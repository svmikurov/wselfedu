"""Null builder."""

from typing import TypeVar

from apps.core.builders.protocol import SpecDtoBuilderProtocol

DtoT = TypeVar('DtoT')
Spec_contra = TypeVar('Spec_contra', contravariant=True)


class NullSpecDtoBuilder(
    SpecDtoBuilderProtocol[
        DtoT,
        Spec_contra,
        DtoT,
    ]
):
    """Null DTO builder with specification."""

    def build(
        self,
        data: DtoT,
        spec: Spec_contra,
    ) -> DtoT:
        """Build the DTO."""
        return data

    @property
    def name(self) -> str:
        """Return null builder name."""
        return 'Null builder'
