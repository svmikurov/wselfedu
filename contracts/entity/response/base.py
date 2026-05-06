"""Protocols for web response interface."""

from typing import Protocol, TypeVar

from contracts.entity.domain.general import DumpModelProtocol, HasDomainStatus
from contracts.entity.general import HasContext, HasExtraContext

from .general import HasHtml

DomainResultStatusT = TypeVar('DomainResultStatusT')
ContextT = DumpModelProtocol[dict[str, str]]


class HtmlResponseProtocol(
    HasDomainStatus[DomainResultStatusT],
    HasContext[ContextT],
    HasExtraContext[ContextT],
    HasHtml,
    Protocol,
):
    """Protocol for response DTO interface."""
