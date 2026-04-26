"""Protocols for web response interface."""

from typing import Protocol, TypeVar

from apps.core.handlers.protocol import HasOob
from interfaces.entity.domain.general import (
    DumpModelProtocol,
    HasDomainStatus,
)
from interfaces.entity.general import HasContext

DomainResultStatusT = TypeVar('DomainResultStatusT')


class OobResponseProtocol(
    HasOob,
    HasDomainStatus[DomainResultStatusT],
    HasContext[DumpModelProtocol[dict[str, str]]],
    Protocol,
):
    """Protocol for response DTO interface."""
