"""Response DTO."""

from typing import Any, Generic, TypeVar

from pydantic import Field

from apps.core.domains.dto import ArbitraryDTO

ResponseStatus = TypeVar('ResponseStatus')
AdaptedDomainResult = TypeVar('AdaptedDomainResult')
ExtraContext = TypeVar('ExtraContext')


class ResponseDTO(
    ArbitraryDTO,
    Generic[ResponseStatus, AdaptedDomainResult, ExtraContext],
):
    """Response adapter DTO."""

    status: ResponseStatus = Field(
        description='Response status',
    )
    context: AdaptedDomainResult = Field(
        description='Domain result data',
    )
    extra_context: ExtraContext | dict[str, Any] = Field(
        description='Additional page context',
        default_factory=dict,
    )


class OobResponseDTO(
    ResponseDTO[ResponseStatus, AdaptedDomainResult, ExtraContext],
    Generic[ResponseStatus, AdaptedDomainResult, ExtraContext],
):
    """Response adapter DTO with Out Of Band."""

    oob_html: str = Field(
        description='Out Of Band',
        default_factory=str,
    )
