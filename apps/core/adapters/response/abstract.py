"""Abstract base classes for response adapter."""

from abc import ABC, abstractmethod
from typing import TypeVar, override

from apps.core.handlers.protocol import AdapterProtocol

ExtraContext = TypeVar('ExtraContext')
DomainResult = TypeVar('DomainResult')
ResponseData = TypeVar('ResponseData')


class AbstractResponseAdapter(
    ABC,
    AdapterProtocol[DomainResult, ExtraContext, ResponseData],
):
    """ABC for response adapter."""

    @override
    @abstractmethod
    def to_response(
        self,
        context: DomainResult,
        extra_context: ExtraContext,
    ) -> ResponseData:
        """Convert domain schema to response representation."""
