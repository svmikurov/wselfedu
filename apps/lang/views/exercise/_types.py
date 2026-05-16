"""Translation exercise types."""

from typing import Any

from kernel.handler.generic import RequestHandler
from ports.contract.entity.domain.general import HasAction
from ports.contract.entity.general import NullProtocol
from ports.contract.enums.exercise import (
    ExerciseAction,
    ExerciseStatus,
)
from ports.interfaces.protocols.request.general import RequestContextProtocol
from ports.interfaces.protocols.web import (
    RequestDataProtocol,
)
from ports.interfaces.schemas.command import UserDataCommand
from ports.interfaces.schemas.response.web.generic import HtmlResponseDTO
from ports.interfaces.typed.web.exercise import (
    PresentationActionDataU,
    TestActionDataU,
)

# FIXME: Fix Any type hint

type RequestParamsT = NullProtocol

type ResponseDtoT = HtmlResponseDTO[
    ExerciseStatus,
    Any,  # Adapted domain result data
    dict[str, Any],  # Extra context
]

type PresentationHandlerT = RequestHandler[
    RequestParamsT,
    RequestContextProtocol,
    RequestDataProtocol[PresentationActionDataU],
    HasAction[ExerciseAction],
    UserDataCommand[HasAction[ExerciseAction]],
    Any,
    ResponseDtoT,
]

type TestHandlerT = RequestHandler[
    RequestParamsT,
    RequestContextProtocol,
    RequestDataProtocol[TestActionDataU],
    HasAction[ExerciseAction],
    UserDataCommand[HasAction[ExerciseAction]],
    Any,
    ResponseDtoT,
]
