"""Language discipline generic UseCase."""

from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from apps.users.models import Person

    from ..types.use_case import (
        BusinessService,
        DetailValidator,
        RegularValidator,
        ResponseAdapter,
    )

RequestData = TypeVar('RequestData')
RequestDTO = TypeVar('RequestDTO')
DomainResult = TypeVar('DomainResult')
ResponseData = TypeVar('ResponseData')


class UseCase(Generic[RequestData, RequestDTO, DomainResult, ResponseData]):
    """UseCase for operations without identifier."""

    def __init__(
        self,
        validator: RegularValidator[RequestData, RequestDTO],
        service: BusinessService[RequestDTO, DomainResult],
        response_adapter: ResponseAdapter[DomainResult, ResponseData],
    ) -> None:
        """Construct the UseCase."""
        self._validator = validator
        self._service = service
        self._response_adapter = response_adapter

    def execute(
        self,
        user: Person,
        request_data: RequestData,
    ) -> ResponseData:
        """Execute the UseCase."""
        validated = self._validator.validate(request_data)
        domain_result = self._service.execute(user, validated)
        result = self._response_adapter.to_response(domain_result)
        return result


class DetailUseCase(
    Generic[RequestData, RequestDTO, DomainResult, ResponseData]
):
    """UseCase for operations with identifier (pk)."""

    def __init__(
        self,
        validator: DetailValidator[RequestData, RequestDTO],
        service: BusinessService[RequestDTO, DomainResult],
        response_adapter: ResponseAdapter[DomainResult, ResponseData],
    ) -> None:
        """Construct the UseCase."""
        self._validator = validator
        self._service = service
        self._response_adapter = response_adapter

    def execute(
        self,
        user: Person,
        request_data: RequestData,
        pk: int,
    ) -> ResponseData:
        """Execute the UseCase."""
        validated = self._validator.validate(request_data, pk=pk)
        domain_result = self._service.execute(user, validated)
        result = self._response_adapter.to_response(domain_result)
        return result
