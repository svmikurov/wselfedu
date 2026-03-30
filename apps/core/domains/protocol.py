"""Protocol for DTO factory."""

from typing import Protocol, TypeVar

Data_contra = TypeVar('Data_contra', contravariant=True)
DumpData_cov = TypeVar('DumpData_cov', covariant=True)
DTO_cov = TypeVar('DTO_cov', covariant=True)

# =================================================
# Null interface
# =================================================


class NullProtocol(Protocol):
    """Nul interface."""


# =================================================
# DTO interface
# =================================================


class DTOProtocol(Protocol[DumpData_cov]):
    """Protocol for DTO interface."""

    def model_dump(self) -> DumpData_cov:
        """Dumb DTO model to dict."""


# =================================================
# Dependencies interface
# =================================================


class DTOFactoryProtocol(Protocol[Data_contra, DTO_cov]):
    """Protocol for DTO factory."""

    def build(self, data: Data_contra) -> DTO_cov:
        """Build DTO."""
