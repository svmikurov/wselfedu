"""Abstract base classes for use cases."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar, override

from apps.core.handlers.protocol import UseCaseProtocol

if TYPE_CHECKING:
    from apps.core.handlers.protocol import (
        DetailParamsProtocol,
        RequestContextProtocol,
    )
    from apps.users.models import Person

__all__ = (
    'AbstractDataUseCase',
    'AbstractDetailUseCase',
)

RequestData = TypeVar('RequestData')
ResponseData = TypeVar('ResponseData')

RequestParams = TypeVar('RequestParams')
RequestContext = TypeVar('RequestContext')
Validated = TypeVar('Validated')
DomainResult = TypeVar('DomainResult')


class AbstractUseCase(
    ABC,
    UseCaseProtocol[RequestParams, RequestContext, Validated, DomainResult],
):
    """ABC for generic use case."""

    @override
    @abstractmethod
    def execute(
        self,
        params: RequestParams,
        context: RequestContext,
        validated: Validated,
    ) -> DomainResult:
        """Execute business logic."""


class AbstractDataUseCase(ABC, Generic[RequestData, ResponseData]):
    """ABC for use case."""

    @abstractmethod
    def execute(self, user: Person, request_data: RequestData) -> ResponseData:
        """Execute use case."""


class AbstractDetailUseCase(ABC, Generic[ResponseData]):
    """ABC for detail use case."""

    @abstractmethod
    def execute(
        self,
        params: DetailParamsProtocol,
        context: RequestContextProtocol,
        data: object,
    ) -> ResponseData:
        """Execute use case."""


class AbstractDetailDataUseCase(ABC, Generic[RequestData, ResponseData]):
    """ABC for detail use case with data."""

    @abstractmethod
    def execute(
        self,
        params: DetailParamsProtocol,
        context: RequestContextProtocol,
        data: RequestData,
    ) -> ResponseData:
        """Execute use case."""
