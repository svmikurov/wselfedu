"""Translation exercise types."""

from typing import Any

from contracts import NullProtocol
from contracts.entity.domain.general import HasAction
from contracts.schemas.response.generic import HtmlResponseDTO
from interfaces.protocols.request.general import RequestContextProtocol
from kernel.handler.generic import RequestHandler
from ports.contract.enums.exercise import (
    ExerciseAction,
    ExerciseStatus,
)
from ports.interfaces.protocols.web import (
    RequestDataProtocol,
)
from ports.interfaces.schemas.command import UserDataCommand

type ResponseDtoT = HtmlResponseDTO[
    ExerciseStatus,
    # FIXME: Fix Any type hint
    Any,  # Adapted domain result data
    dict[str, Any],  # Extra context
]
type HandlerT = RequestHandler[
    NullProtocol,  # No request parameters
    RequestContextProtocol,  # Authentication required
    RequestDataProtocol[dict[str, Any]],  # Exercise performing request data
    HasAction[ExerciseAction],  # Validated data
    UserDataCommand[HasAction[ExerciseAction]],  # User's request command
    # FIXME: Fix Any type hint
    Any,  # Domain result
    ResponseDtoT,  # Response data for page template
]
