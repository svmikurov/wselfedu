"""Translation exercise types."""

from typing import Any

from apps.core.assemblers.command import UserDataCommand
from apps.core.handlers.generic import RequestHandler
from apps.core.handlers.protocol import (
    RequestContextProtocol,
    RequestDataProtocol,
)
from interfaces import NullProtocol
from interfaces.enums.exercise import (
    ExerciseAction,
    ExerciseStatus,
)
from interfaces.protocols.domain.general import HasAction
from interfaces.schemas.response.generic import OobResponseDTO

type ResponseDtoT = OobResponseDTO[
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
