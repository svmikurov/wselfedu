"""WEB response DTO field mixins."""

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

DomainResultStatusT = TypeVar('DomainResultStatusT')
AdaptedDomainResultT = TypeVar('AdaptedDomainResultT')
ExtraContextT = TypeVar('ExtraContextT')


class DomainStatusField(BaseModel, Generic[DomainResultStatusT]):
    """Provides domain status DTO's field."""

    domain_status: DomainResultStatusT = Field(
        description='Domain result status',
    )


class ContextField(BaseModel, Generic[AdaptedDomainResultT]):
    """Provides context DTO's field."""

    context: AdaptedDomainResultT = Field(
        description='Response context with adapted domain result data',
    )


class ExtraContextField(BaseModel, Generic[ExtraContextT]):
    """Provides extra context DTO's field."""

    extra_context: ExtraContextT | dict[str, Any] = Field(
        description='Extra context for response',
        default_factory=dict,
    )


class OobField(BaseModel):
    """Provides "Out Of Band" html DTO's field."""

    oob_html: str = Field(
        description='Out Of Band html',
        default_factory=str,
    )
