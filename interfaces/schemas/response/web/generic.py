"""General WEB response contracts."""

from typing import Generic

from contracts.schemas.base import ArbitraryDTO
from contracts.schemas.response._types import (
    AdaptedDomainResultT,
    DomainResultStatusT,
    ExtraContextT,
)
from contracts.schemas.response.mixins import (
    ContextField,
    DomainStatusField,
    ExtraContextField,
    OobField,
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


class OobResponseDTO(
    OobField,
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
    oob_html : `str`
        Out Of Band html.
    """
