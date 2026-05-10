"""Abstract base class for request parameters query parser."""

from abc import ABC, abstractmethod
from typing import TypeVar, override

from kernel.parser.request import RequestParamsQueryParserProtocol

QueryDataT = TypeVar('QueryDataT')
QueryTypeT = TypeVar('QueryTypeT')

__all__ = ('AbstractRequestParamsQueryParser',)


class AbstractRequestParamsQueryParser(
    ABC,
    RequestParamsQueryParserProtocol[QueryDataT, QueryTypeT],
):
    """ABC for request parameters query parser."""

    @override
    @abstractmethod
    def parse(self, query: QueryDataT) -> QueryTypeT:
        """Parse request parameters query."""
