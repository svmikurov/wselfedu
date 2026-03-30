"""Abstract base classes for response adapter."""

from abc import ABC, abstractmethod
from typing import TypeVar, override

from apps.core.handlers.protocol import AdapterProtocol

DomainResult = TypeVar('DomainResult')
ExtraContext = TypeVar('ExtraContext')
ResponseData = TypeVar('ResponseData')


class AbstractResponseAdapter(
    ABC,
    AdapterProtocol[
        DomainResult,
        ExtraContext,
        ResponseData,
    ],
):
    """ABC for response adapter.

    Converts domain DTO to Web response format.
    Includes extra context needed for server-rendered templates.
    """

    @override
    @abstractmethod
    def to_response(
        self,
        domain_result: DomainResult,
        request_context: ExtraContext,
    ) -> ResponseData:
        """Convert domain schema to response representation."""
