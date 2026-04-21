"""General eb response contracts."""

from typing import Generic

from apps.core.domains.dto import ArbitraryDTO

from ._types import AdaptedDomainResultT, DomainResultStatusT, ExtraContextT
from .mixins import (
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
    """Response adapter DTO."""


class OobResponseDTO(
    OobField,
    ResponseDTO[DomainResultStatusT, AdaptedDomainResultT, ExtraContextT],
    Generic[DomainResultStatusT, AdaptedDomainResultT, ExtraContextT],
):
    """Response adapter DTO with Out Of Band."""
