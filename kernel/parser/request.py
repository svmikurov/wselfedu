"""Protocol for request parameters query parser."""

from typing import Protocol, TypeVar

QueryData_contra = TypeVar('QueryData_contra', contravariant=True)
QueryType_co = TypeVar('QueryType_co', covariant=True)

__all__ = ('RequestParamsQueryParserProtocol',)


class RequestParamsQueryParserProtocol(
    Protocol[QueryData_contra, QueryType_co]
):
    """Protocol for request parameters query parser."""

    def parse(self, query: QueryData_contra) -> QueryType_co:
        """Parse request parameters query."""
