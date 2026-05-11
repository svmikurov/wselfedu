"""Protocol for request interface."""

from typing import Protocol

from ports.contract.entity.general import HasUser


class HasIsHtmx(Protocol):
    """Protocol for has *is_htmx* interface."""

    is_htmx: bool


class RequestContextProtocol(
    HasUser,
    Protocol,
):
    """Protocol for request context DTO."""
