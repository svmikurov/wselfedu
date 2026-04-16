"""Protocols for DTO infrastructure interface."""

from typing import Protocol, TypeVar

DumpData_co = TypeVar('DumpData_co', covariant=True)


# REVIEW: Temporary unused protocol
class DumpModelProtocol(Protocol[DumpData_co]):
    """Protocol for *model_dump* interface."""

    def model_dump(self) -> DumpData_co:
        """Dumb DTO model to dict."""
