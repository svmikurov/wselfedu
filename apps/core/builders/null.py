"""Null builder."""

from . import aliases
from .protocol import SpecDtoBuilderProtocol


class NullSpecDtoBuilder(
    SpecDtoBuilderProtocol[
        aliases.DtoT,
        aliases.Spec_contra,
        aliases.DtoT,
    ]
):
    """Null DTO builder with specification."""

    def build(
        self,
        data: aliases.DtoT,
        spec: aliases.Spec_contra,
    ) -> aliases.DtoT:
        """Build the DTO."""
        return data
