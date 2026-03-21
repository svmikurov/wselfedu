"""Protocol for DTO factory."""

from typing import Protocol, TypeVar

Data_contra = TypeVar('Data_contra', contravariant=True)
DTO_cov = TypeVar('DTO_cov', covariant=True)


class DTOFactoryProtocol(Protocol[Data_contra, DTO_cov]):
    """Protocol for DTO factory."""

    def build(self, data: Data_contra) -> DTO_cov:
        """Build DTO."""
