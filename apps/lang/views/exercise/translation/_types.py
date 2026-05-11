"""Translation exercise types."""

from typing import Any

from interfaces.protocols.request.general import RequestContextProtocol
from kernel.handler.generic import RequestHandler
from ports.contract.entity.domain.general import HasAction
from ports.contract.entity.general import NullProtocol
from ports.contract.enums.exercise import (
    ExerciseAction,
    ExerciseStatus,
)
from ports.interfaces.protocols.web import (
    RequestDataProtocol,
)
from ports.interfaces.schemas.command import UserDataCommand
from ports.interfaces.schemas.response.web.generic import HtmlResponseDTO

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
