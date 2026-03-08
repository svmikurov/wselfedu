"""Generic request handlers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

from .protocol import (
    DetailParamsProtocol,
    DetailValidator,
    RequestContextProtocol,
    RequestDataProtocol,
    RequestResultProtocol,
)

if TYPE_CHECKING:
    from apps.users.models import Person

    from .protocol import (
        ContextResponseAdapter,
        DetailUseCase,
        RegularValidator,
        ResourceValidator,
        ResponseAdapter,
        ResponseAdapterDeprecated,
        UseCase,
    )

RequestData = TypeVar('RequestData')
Validated = TypeVar('Validated')
DomainResult = TypeVar('DomainResult')
ResponseData = TypeVar('ResponseData')


class RegularRequestHandler(
    Generic[RequestData, Validated, DomainResult, ResponseData]
):
    """Regular request handler."""

    def __init__(
        self,
        validator: RegularValidator[RequestData, Validated],
        use_case: UseCase[Validated, DomainResult],
        adapter: ResponseAdapterDeprecated[DomainResult, ResponseData],
    ) -> None:
        """Construct the handler."""
        self._validator = validator
        self._use_case = use_case
        self._adapter = adapter

    def execute(
        self,
        user: Person,
        request_data: RequestData,
    ) -> ResponseData:
        """Handle the request."""
        validated_data = self._validator.validate(request_data)
        result_data = self._use_case.execute(user, validated_data)
        response_data = self._adapter.to_response(result_data)
        return response_data


# DEPRECATED: Use DetailRequestHandler
class ResourceRequestHandler(
    Generic[RequestData, Validated, DomainResult, ResponseData]
):
    """Regular request handler for operations with identifier (pk)."""

    def __init__(
        self,
        validator: ResourceValidator[RequestData, Validated],
        use_case: UseCase[Validated, DomainResult],
        adapter: ResponseAdapterDeprecated[DomainResult, ResponseData],
    ) -> None:
        """Construct the handler."""
        self._validator = validator
        self._use_case = use_case
        self._adapter = adapter

    def execute(
        self,
        user: Person,
        request_data: RequestData,
        pk: int,
    ) -> ResponseData:
        """Execute."""
        validated = self._validator.validate(request_data, pk=pk)
        domain_result = self._use_case.execute(user, validated)
        result = self._adapter.to_response(domain_result)
        return result


class DetailRequestHandler(Generic[Validated, DomainResult]):
    """Detail request handler for operations with identifier (pk)."""

    def __init__(
        self,
        validator: DetailValidator[Validated],
        use_case: DetailUseCase[Validated, DomainResult],
        adapter: ResponseAdapter[DomainResult],
    ) -> None:
        """Construct the handler."""
        self._validator = validator
        self._use_case = use_case
        self._adapter = adapter

    def execute(
        self,
        params: DetailParamsProtocol,
        context: RequestContextProtocol,
        data: RequestDataProtocol,
    ) -> RequestResultProtocol:
        """Execute."""
        validated = self._validator.validate(data)
        domain_result = self._use_case.execute(params, context, validated)
        result = self._adapter.to_response(domain_result)
        return result


class ContextRequestHandler(Generic[Validated, DomainResult]):
    """Context request handler for operations with identifier (pk).
    
    Passes the request context to the adapter.
    """

    def __init__(
        self,
        validator: DetailValidator[Validated],
        use_case: DetailUseCase[Validated, DomainResult],
        adapter: ContextResponseAdapter[DomainResult],
    ) -> None:
        """Construct the handler."""
        self._validator = validator
        self._use_case = use_case
        self._adapter = adapter

    def execute(
        self,
        params: DetailParamsProtocol,
        context: RequestContextProtocol,
        data: RequestDataProtocol,
    ) -> RequestResultProtocol:
        """Execute."""
        validated = self._validator.validate(data)
        domain_result = self._use_case.execute(params, context, validated)
        result = self._adapter.to_response(domain_result, context)
        return result
