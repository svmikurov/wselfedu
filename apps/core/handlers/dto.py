"""Request handler's DTOs.

Creates in view to pass to the handler's 'execute()' method.
"""

from typing import Generic, TypeVar

from pydantic import Field

from apps.core.domains.dto import ArbitraryDTO, BaseDTO
from apps.users.models import Person

__all__ = (
    # Parameters
    'QueryRequestParams',
    'DetailRequestParams',
    'DetailQueryRequestParams',
    # Context
    'RequestContext',
    # Data
    'RequestData',
    # Response data
    'RequestResult',
)

QueryData = TypeVar('QueryData')
Data = TypeVar('Data')
Validated = TypeVar('Validated')
ResultType = TypeVar('ResultType')


# =================================================
# Request parameters
# =================================================


class QueryRequestParams(BaseDTO, Generic[QueryData]):
    """Query request parameters DTO."""

    query: QueryData = Field(
        description='Request query',
    )


class DetailRequestParams(BaseDTO):
    """Detail request parameters DTO."""

    pk: int


class DetailQueryRequestParams(
    QueryRequestParams[QueryData],
    DetailRequestParams,
):
    """Detail query request parameters DTO."""


# =================================================
# Request context
# =================================================


class RequestContext(ArbitraryDTO):
    """Request context."""

    user: Person


# =================================================
# Request data
# =================================================


class RequestData(BaseDTO, Generic[Data]):
    """Request data."""

    data: Data = Field(
        description=Field('Request data'),
    )


# =================================================
# Response data context
# =================================================


class RequestResult(BaseDTO, Generic[ResultType]):
    """Result of request handling."""

    context: ResultType = Field(
        description=Field('Response context'),
    )
