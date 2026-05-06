"""General WEB response contracts."""

from typing import Generic

from contracts.schemas.base import ArbitraryDTO
from contracts.schemas.response.mixins import (
    ContextField,
    DomainStatusField,
    ExtraContextField,
    HtmlField,
)
from contracts.schemas.response.types import (
    AdaptedDomainResultT,
    DomainResultStatusT,
    ExtraContextT,
)


class ResponseDTO(
    DomainStatusField[DomainResultStatusT],
    ContextField[AdaptedDomainResultT],
    ExtraContextField[ExtraContextT],
    ArbitraryDTO,
    Generic[DomainResultStatusT, AdaptedDomainResultT, ExtraContextT],
):
    """Response DTO.

    Parameter
    ---------
    domain_status : `DomainResultStatusT`
        Domain result status.
    context : `AdaptedDomainResultT`
        Response context with adapted domain result data.
    extra_context : `ExtraContextT`
        Extra context for response.
    """


class HtmlResponseDTO(
    HtmlField,
    ResponseDTO[DomainResultStatusT, AdaptedDomainResultT, ExtraContextT],
    Generic[DomainResultStatusT, AdaptedDomainResultT, ExtraContextT],
):
    """Response DTO with Out Of Band.

    Parameter
    ---------
    domain_status : `DomainResultStatusT`
        Domain result status.
    context : `AdaptedDomainResultT`
        Response context with adapted domain result data.
    extra_context : `ExtraContextT`
        Extra context for response.
    html : `str`
        Out Of Band html.
    """
