"""Protocols for web response interface."""

from typing import Protocol, TypeVar

from ports.contract.entity.domain.general import (
    DumpModelProtocol,
    HasDomainStatus,
)
from ports.contract.entity.general import HasContext, HasExtraContext
from ports.contract.response.general import HasHtml

DomainResultStatusT = TypeVar('DomainResultStatusT')
ContextT = DumpModelProtocol[dict[str, str]]


class HtmlResponseProtocol(
    HasDomainStatus[DomainResultStatusT],
    HasContext[ContextT],
    HasExtraContext[ContextT],
    HasHtml,
    Protocol,
):
    """Protocol for response DTO interface.

    Parameters
    ----------
    domain_status : `DomainResultStatusT`
        Domain result status.
    context : `DumpModelProtocol[dict[str, str]]`
        Response context.
    extra_context : `DumpModelProtocol[dict[str, str]]`
        Response extra context.
    html : `str`
        HTML code.

    """
