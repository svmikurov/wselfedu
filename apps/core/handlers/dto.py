"""Request handler DTOs."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from apps.users.models import Person


class NullParams(BaseModel):
    """Null request parameters DTO."""


class RequestContext(BaseModel):
    """Request context."""

    user: Person

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra='forbid',
        frozen=True,
    )


class DetailParams(BaseModel):
    """Detail request parameters."""

    pk: int = Field(
        description='Resource pk',
    )

    model_config = ConfigDict(
        extra='forbid',
        frozen=True,
    )


class RequestData(BaseModel):
    """Request data."""

    query: dict[str, Any] = Field(
        description=Field('Request data'),
    )


class RequestResult(BaseModel):
    """Result of request handling."""

    context: dict[str, Any] = Field(
        description=Field('Response context'),
    )
