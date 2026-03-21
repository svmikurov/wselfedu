"""Protocol for request parameters query parser."""

from typing import Protocol, TypeVar

QueryData_contra = TypeVar('QueryData_contra', contravariant=True)
QueryType_cov = TypeVar('QueryType_cov', covariant=True)

__all__ = ('RequestParamsQueryParserProtocol',)


class RequestParamsQueryParserProtocol(
    Protocol[QueryData_contra, QueryType_cov]
):
    """Protocol for request parameters query parser."""

    def parse(self, query: QueryData_contra) -> QueryType_cov:
        """Parse request parameters query."""
