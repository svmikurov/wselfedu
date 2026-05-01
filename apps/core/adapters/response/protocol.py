"""Protocol for response adapter interface."""

from typing import Protocol, TypeVar

from utils.audit.protocol import Auditable

Context_contra = TypeVar('Context_contra', contravariant=True)
UseCaseResult_contra = TypeVar('UseCaseResult_contra', contravariant=True)
ResponseData_co = TypeVar('ResponseData_co', covariant=True)


class AdapterProtocol(
    Auditable,
    Protocol[UseCaseResult_contra, Context_contra, ResponseData_co],
):
    """Protocol for response adapter interface."""

    def to_response(
        self,
        domain_result: UseCaseResult_contra,
        request_context: Context_contra,
    ) -> ResponseData_co:
        """Convert to response."""
