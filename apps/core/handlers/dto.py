"""Request handler DTOs."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from apps.core.domains.base_dto import BaseDTO
from apps.users.models import Person

__all__ = (
    # Parameters
    'DetailParams',
    'QueryParams',
    # Context
    'RequestContext',
    # Data
    'RequestData',
    # Response data
    'RequestResult',
)


class NullParams(BaseDTO):
    """Null request parameters DTO."""


# =================================================
# Request parameters
# =================================================


class DetailParams(BaseDTO):
    """Detail request parameters."""

    pk: int = Field(
        description='Resource pk',
    )


class QueryParams(BaseDTO):
    """Request query parameters."""

    query: dict[str, str] = Field(
        description='Request query',
    )


class RequestParams(BaseDTO):
    """Request parameters."""

    pk: int
    query: dict[str, str] = Field(
        description='Request query',
    )


# =================================================
# Request context
# =================================================


class RequestContext(BaseModel):
    """Request context."""

    user: Person

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra='forbid',
        frozen=True,
    )


# =================================================
# Request data
# =================================================


class RequestData(BaseDTO):
    """Request data."""

    query: dict[str, Any] = Field(
        description=Field('Request data'),
    )


# =================================================
# Response data context
# =================================================


class RequestResult(BaseDTO):
    """Result of request handling."""

    context: dict[str, Any] = Field(
        description=Field('Response context'),
    )
