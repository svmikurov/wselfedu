"""Protocol for DTO formatter."""

from typing import Protocol, TypeVar

ConfigurationT = TypeVar('ConfigurationT')

Data_contra = TypeVar('Data_contra', contravariant=True)
Spec_contra = TypeVar('Spec_contra', contravariant=True)
Dto_co = TypeVar('Dto_co', covariant=True)


class ConfFormatterProtocol(Protocol[Data_contra, Spec_contra, Dto_co]):
    """Protocol for a DTO formatter that follows the configuration."""

    def format(self, data: Data_contra, conf: Spec_contra) -> Dto_co:
        """Build a DTO according to the configuration."""
