"""Mathematical discipline handler types."""

from typing import Any

from apps.core.handlers.dto import (
    RequestContext,
    RequestData,
)
from apps.core.validators.request.null import NullValidator
from apps.math.domains.dto import StudentExerciseDTO
from kernel.handler.generic import RequestHandler
from ports.interfaces.protocols.web import RequestDataProtocol

# FIXME:
StudentExerciseListHandler = RequestHandler[
    Any,
    RequestContext,
    RequestData[dict[str, str]],
    NullValidator[RequestDataProtocol[Any]],
    list[StudentExerciseDTO],
    Any,
    Any,
]
