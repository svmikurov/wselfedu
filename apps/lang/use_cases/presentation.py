"""Get presentation UseCase."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, TypeVar

from .. import schemas, types
from ..schemas import dto

if TYPE_CHECKING:
    from apps.users.models import Person

    from ..types.presentation import (
        BusinessService,
        ResponseAdapter,
        Validator,
    )

RequestData = TypeVar('RequestData')
RequestDTO = TypeVar('RequestDTO')
DomainResult = TypeVar('DomainResult')
ResponseData = TypeVar('ResponseData')


class PresentationUseCase(
    Generic[RequestData, RequestDTO, DomainResult, ResponseData]
):
    """Presentation UseCase."""

    def __init__(
        self,
        validator: Validator[RequestData, RequestDTO],
        service: BusinessService[RequestDTO, DomainResult],
        response_adapter: ResponseAdapter[DomainResult, ResponseData],
    ) -> None:
        """Construct the UseCase."""
        self._validator = validator
        self._service = service
        self._response_adapter = response_adapter

    def execute(self, user: Person, request_data: RequestData) -> ResponseData:
        """Get presentation case."""
        validated = self._validator.validate(request_data)
        domain_result = self._service.execute(user, validated)
        result = self._response_adapter.to_response(domain_result)
        return result


class ApiPresentationUseCase(
    PresentationUseCase[
        dict[str, Any],
        schemas.PresentationRequest,
        dto.PresentationCase,
        types.TranslationAPI,
    ]
):
    """Api presentation UseCase."""


class WebPresentationUseCase(
    PresentationUseCase[
        dict[str, Any],
        schemas.PresentationRequest,
        dto.PresentationCase,
        types.TranslationWEB,
    ]
):
    """Presentation UseCase."""
