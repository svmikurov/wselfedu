"""Response's general interface."""

from typing import Protocol, TypeVar

from ports.contract.entity.domain.general import (
    DumpModelProtocol,
    HasDomainStatus,
)
from ports.contract.entity.general import HasContext, HasExtraContext

_DTO = DumpModelProtocol[dict[str, str]]
DomainResultStatusT = TypeVar('DomainResultStatusT')
ContextT = TypeVar('ContextT', bound=_DTO)
ExtraContextT = TypeVar('ExtraContextT', bound=_DTO)


class HasHtml(Protocol):
    """Protocol for has *html* DTO field."""

    html: str


class HtmlResponseProtocol(
    HasDomainStatus[DomainResultStatusT],
    HasContext[ContextT],
    HasExtraContext[ExtraContextT],
    HasHtml,
    Protocol,
):
    """Protocol for response DTO interface.

    Parameters
    ----------
    domain_status : `DomainResultStatusT`
        Domain result status.
    context : `ContextT`
        Response context.
    extra_context : `ExtraContextT`
        Response extra context.
    html : `str`
        HTML code.

    """
