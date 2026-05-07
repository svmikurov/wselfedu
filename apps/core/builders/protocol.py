"""Protocol for DTO builder."""

from typing import Protocol, TypeVar

from . import aliases

ConfigurationT = TypeVar('ConfigurationT')


class DtoBuilderProtocol(Protocol[aliases.DTO_contra, aliases.DTO_co]):
    """Protocol for a DTO builder interface."""

    def build(
        self,
        data: aliases.DTO_contra,
    ) -> aliases.DTO_co:
        """Build the DTO."""


class SpecDtoBuilderProtocol(
    Protocol[
        aliases.DTO_contra,
        aliases.Spec_contra,
        aliases.DTO_co,
    ]
):
    """Protocol for a DTO builder that follows the specification."""

    def build(
        self,
        data: aliases.DTO_contra,
        spec: aliases.Spec_contra,
    ) -> aliases.DTO_co:
        """Build a DTO according to the specification."""


class ConfDtoBuilderProtocol(
    Protocol[
        aliases.DTO_contra,
        aliases.Spec_contra,
        aliases.DTO_co,
    ]
):
    """Protocol for a DTO builder that follows the configuration."""

    def build(
        self,
        data: aliases.DTO_contra,
        conf: aliases.Spec_contra,
    ) -> aliases.DTO_co:
        """Build a DTO according to the configuration."""
