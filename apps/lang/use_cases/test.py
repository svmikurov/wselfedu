"""Language discipline test exercise UseCase."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .. import schemas
from . import UseCase

if TYPE_CHECKING:
    from apps.users.models import Person

    from ..types.use_case import (
        BusinessService,
        DetailValidator,
        ResponseAdapter,
    )

type RequestData = dict[str, Any]
type RequestDTO = schemas.DetailTestRequestDTO
type DomainResult = schemas.Case | schemas.Explanation
type ResponseData = schemas.TestResponseData


class WebTestUseCase(
    UseCase[RequestData, RequestDTO, DomainResult, ResponseData]
):
    """Web translation study test exercise UseCase."""


class AssignmentUseCase:
    """Web translation test exercise UseCase with assignment ID."""

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
        assignment_id: int,
    ) -> ResponseData:
        """Execute the UseCase."""
        validated = self._validator.validate(request_data, assignment_id)
        domain_result = self._service.execute(user, validated)
        result = self._response_adapter.to_response(domain_result)
        return result
