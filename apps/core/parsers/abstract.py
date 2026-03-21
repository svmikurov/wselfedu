"""Abstract base class for request parameters query parser."""

from abc import ABC, abstractmethod
from typing import TypeVar, override

from .protocol import RequestParamsQueryParserProtocol

QueryData = TypeVar('QueryData')
QueryType = TypeVar('QueryType')


class AbstractRequestParamsQueryParser(
    ABC,
    RequestParamsQueryParserProtocol[QueryData, QueryType],
):
    """ABC for request parameters query parser."""

    @override
    @abstractmethod
    def parse(self, query: QueryData) -> QueryType:
        """Parse request parameters query."""
