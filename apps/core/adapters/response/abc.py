"""Abstract base classes for response adapter."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, override

from apps.core.handlers.protocol import AdapterProtocol

RequestContext = TypeVar('RequestContext')
DomainResult = TypeVar('DomainResult')
ResponseData = TypeVar('ResponseData')


class AbstractResponseAdapter(
    ABC, AdapterProtocol[DomainResult, RequestContext, ResponseData]
):
    """ABC for response adapters."""

    @override
    @abstractmethod
    def to_response(
        self,
        schema: DomainResult,
        request_context: RequestContext,
    ) -> ResponseData:
        """Convert domain schema to response representation."""


class AbstractSimpleResponseAdapter(ABC, Generic[DomainResult, ResponseData]):
    """ABC for simple response adapters."""

    @abstractmethod
    def to_response(self, schema: DomainResult) -> ResponseData:
        """Convert domain schema to response representation."""
