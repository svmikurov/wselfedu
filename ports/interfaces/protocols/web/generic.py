"""General WEB response contracts."""

from typing import Generic, TypeVar

from ports.interfaces.schemas.base import ArbitraryDTO
from ports.interfaces.schemas.response.web.mixins import (
    ContextField,
    DomainStatusField,
    ExtraContextField,
    HtmlField,
)

DomainResultStatusT = TypeVar('DomainResultStatusT')
AdaptedDomainResultT = TypeVar('AdaptedDomainResultT')
ExtraContextT = TypeVar('ExtraContextT')


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
