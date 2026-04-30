"""Protocols for web response interface."""

from typing import Protocol, TypeVar

from contracts.entity.domain.general import DumpModelProtocol, HasDomainStatus
from contracts.entity.general import HasContext, HasExtraContext

from .general import HasOob

DomainResultStatusT = TypeVar('DomainResultStatusT')
ContextT = DumpModelProtocol[dict[str, str]]


class OobResponseProtocol(
    HasDomainStatus[DomainResultStatusT],
    HasContext[ContextT],
    HasExtraContext[ContextT],
    HasOob,
    Protocol,
):
    """Protocol for response DTO interface."""
