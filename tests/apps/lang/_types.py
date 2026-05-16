"""Test types."""

from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from kernel.handler.generic import RequestHandler
from ports.interfaces.schemas.request.handler import (
    RequestContext,
    RequestData,
)
from ports.interfaces.typed.web.exercise import ExerciseActionU

ParamsT = TypeVar('ParamsT')

PresentationHandlerT = RequestHandler[Any, Any, Any, Any, Any, Any, Any]
TestHandlerT = RequestHandler[Any, Any, Any, Any, Any, Any, Any]


@dataclass(frozen=True)
class RequestArgs(Generic[ParamsT]):
    """Handler request parameters data."""

    params: ParamsT
    context: RequestContext
    data: RequestData[ExerciseActionU]
