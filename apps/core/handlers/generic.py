"""Generic request handlers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from apps.users.models import Person

    from .protocols import (
        BusinessService,
        DetailValidator,
        RegularValidator,
        ResponseAdapter,
        SimpleService,
    )

RequestData = TypeVar('RequestData')
RequestDTO = TypeVar('RequestDTO')
DomainResult = TypeVar('DomainResult')
ResponseData = TypeVar('ResponseData')


class SimpleHandler(Generic[DomainResult, ResponseData]):
    """Simple request handler."""

    def __init__(
        self,
        service: SimpleService[DomainResult],
        adapter: ResponseAdapter[DomainResult, ResponseData],
    ) -> None:
        """Construct the handler."""
        self._service = service
        self._adapter = adapter

    def execute(self, user: Person) -> ResponseData:
        """Execute."""
        domain_result = self._service.execute(user)
        result = self._adapter.to_response(domain_result)
        return result


class RegularRequestHandler(
    Generic[RequestData, RequestDTO, DomainResult, ResponseData]
):
    """Regular request handler."""

    def __init__(
        self,
        validator: RegularValidator[RequestData, RequestDTO],
        service: BusinessService[RequestDTO, DomainResult],
        adapter: ResponseAdapter[DomainResult, ResponseData],
    ) -> None:
        """Construct the handler."""
        self._validator = validator
        self._service = service
        self._adapter = adapter

    def execute(
        self,
        user: Person,
        request_data: RequestData,
    ) -> ResponseData:
        """Handle the request."""
        validated_data = self._validator.validate(request_data)
        result_data = self._service.execute(user, validated_data)
        response_data = self._adapter.to_response(result_data)
        return response_data


class DetailRequestHandler(
    Generic[RequestData, RequestDTO, DomainResult, ResponseData]
):
    """Regular request handler for operations with identifier (pk)."""

    def __init__(
        self,
        validator: DetailValidator[RequestData, RequestDTO],
        service: BusinessService[RequestDTO, DomainResult],
        adapter: ResponseAdapter[DomainResult, ResponseData],
    ) -> None:
        """Construct the handler."""
        self._validator = validator
        self._service = service
        self._adapter = adapter

    def execute(
        self,
        user: Person,
        request_data: RequestData,
        pk: int,
    ) -> ResponseData:
        """Execute."""
        validated = self._validator.validate(request_data, pk=pk)
        domain_result = self._service.execute(user, validated)
        result = self._adapter.to_response(domain_result)
        return result
