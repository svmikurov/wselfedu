"""Protocols for web response interface."""

from typing import Protocol

from apps.core.handlers.protocol import HasOob
from interfaces.protocols.domain.general import (
    DumpModelProtocol,
    HasDomainStatus,
)
from interfaces.protocols.general import HasContext

from ._types import DomainResultStatusT


class OobResponseProtocol(
    HasOob,
    HasDomainStatus[DomainResultStatusT],
    HasContext[DumpModelProtocol[dict[str, str]]],
    Protocol,
):
    """Protocol for response DTO interface."""
