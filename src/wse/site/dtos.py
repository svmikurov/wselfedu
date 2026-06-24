"""Django site DTOs."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class NullDTO:
    """Null DTO."""


@dataclass(frozen=True, slots=True)
class RequestContext:
    """Request context DTO."""


@dataclass(frozen=True, slots=True)
class RequestData:
    """Request data DTO."""

    data: dict[str, Any]
