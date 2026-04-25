"""Create exercise task validator."""

import logging

from pydantic import ValidationError

from apps.core.handlers.protocol import RequestDataProtocol
from interfaces.enums.exercise import ExerciseAction
from interfaces.protocols.domain.general import (
    ActionTyped,
    HasAction,
)
from interfaces.schemas.request.exercise import ExerciseRequestDTO

from ..abstract import AbstractRequestValidator

log = logging.getLogger(__name__)

type _DataT = RequestDataProtocol[ActionTyped]
type _ValidatedT = HasAction[ExerciseAction]


class CreateExerciseTaskValidator(
    AbstractRequestValidator[_DataT, _ValidatedT],
):
    """Create exercise task WEB request data validator."""

    def validate(self, data: _DataT) -> _ValidatedT:
        """Validate test exercise user's answer data."""
        try:
            return ExerciseRequestDTO(
                action=ExerciseAction(data.data['action']),
            )
        except ValidationError as exc:
            log.error(
                f'WEB request data parameters validation error: {exc}\n'
                f'Request data: {data!r}'
            )
            raise
        except Exception as exc:
            log.error(
                f'WEB request data parameters unexpected error: {exc}\n'
                f'Request data: {data!r}'
            )
            raise
