"""Django site DTOs."""

from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

from . import exceptions
from .interfaces.protocols import HasData

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

    session_id: str = field(
        metadata={'description': 'Task session identifier'},
    )

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not isinstance(self.session_id, str):
            raise exceptions.ValidationError(
                f'Expected string type for session identifier, '
                f'got{type(self.session_id).__name__}'
            )


@dataclass(frozen=True, slots=True)
class RequestData:
    """Request data DTO."""

    data: dict[str, Any]


# Response


@dataclass(frozen=True, slots=True)
class ResponseDto(Generic[T]):
    """Response DTO."""

    context: T
