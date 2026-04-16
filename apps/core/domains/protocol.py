"""Protocol for DTO factory."""

from typing import Protocol, TypeVar

Data_contra = TypeVar('Data_contra', contravariant=True)
DumpData_co = TypeVar('DumpData_co', covariant=True)
DTO_co = TypeVar('DTO_co', covariant=True)

# =================================================
# DTO interface
# =================================================


class DTOProtocol(Protocol[DumpData_co]):
    """Protocol for DTO interface."""

    def model_dump(self) -> DumpData_co:
        """Dumb DTO model to dict."""


# =================================================
# Dependencies interface
# =================================================


class DTOFactoryProtocol(Protocol[Data_contra, DTO_co]):
    """Protocol for DTO factory."""

    def build(self, data: Data_contra) -> DTO_co:
        """Build DTO."""
