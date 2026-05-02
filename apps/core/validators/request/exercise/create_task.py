"""Exercise task action validator."""

import logging

from pydantic import ValidationError

from apps.core.handlers.protocol import RequestDataProtocol
from contracts.entity.domain.general import ActionTyped, HasAction
from contracts.enums.exercise import ExerciseAction
from contracts.schemas.request.exercise import ExerciseRequestDTO
from utils.audit.base import BaseAuditable

from ..abstract import AbstractRequestValidator

log = logging.getLogger(__name__)

type _DataT = RequestDataProtocol[ActionTyped]
type _ValidatedT = HasAction[ExerciseAction]


class CreateExerciseTaskValidator(
    BaseAuditable,
    AbstractRequestValidator[_DataT, _ValidatedT],
):
    """Request data action validator."""

    def validate(self, data: _DataT) -> _ValidatedT:
        """Validate the request data."""
        try:
            return ExerciseRequestDTO(
                action=ExerciseAction(data.data['action']),
            )
        except ValidationError as exc:
            log.error(
                f'WEB request data validation error: {exc}\n'
                f'Request data: {data!r}'
            )
            raise
        except Exception as exc:
            log.error(
                f'WEB request data unexpected error: {exc}\n'
                f'Request data: {data!r}'
            )
            raise
