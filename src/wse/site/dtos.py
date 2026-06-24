"""Django site DTOs."""

from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from .protocols import HasData

T = TypeVar('T')

# Request parameter attribute type vars
QueryT = TypeVar('QueryT')
ContextT = TypeVar('ContextT')
DataT = TypeVar('DataT', bound=HasData[dict[str, Any]])


@dataclass(frozen=True, slots=True)
class NullDTO:
    """Null DTO."""


# Request


@dataclass(frozen=True, slots=True)
class RequestContext:
    """Request context DTO."""


@dataclass(frozen=True, slots=True)
class RequestData:
    """Request data DTO."""

    data: dict[str, Any]


@dataclass(frozen=True, slots=True)
class RequestParams(Generic[QueryT, ContextT, DataT]):
    """Request handling parameters DTO."""

    query: QueryT
    context: ContextT
    data: DataT


# Response


@dataclass(frozen=True, slots=True)
class ResponseDto(Generic[T]):
    """Response DTO."""

    context: T
