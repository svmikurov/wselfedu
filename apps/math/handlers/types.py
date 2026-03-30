"""Mathematical discipline handler types."""

from typing import Any

from apps.core.handlers.dto import (
    RequestContext,
    RequestData,
)
from apps.core.handlers.generic import RequestHandler
from apps.core.handlers.protocol import RequestDataProtocol
from apps.core.validators.request.null import NullValidator
from apps.math.domains.dto import StudentExerciseDTO

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
