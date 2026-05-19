"""Test types."""

from dataclasses import dataclass
from typing import Generic, TypeVar

from ports.interfaces.request_data.web.exercise import ExerciseDataU
from ports.interfaces.schemas.request.handler import (
    RequestContext,
    RequestData,
)

ParamsT = TypeVar('ParamsT')


@dataclass(frozen=True)
class RequestArgs(Generic[ParamsT]):
    """Handler request parameters data."""

    params: ParamsT
    context: RequestContext
    data: RequestData[ExerciseDataU]
