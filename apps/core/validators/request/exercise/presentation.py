"""Presentation process exercise validator."""

import logging

from pydantic import ValidationError

from apps.core.domains.exercise.enums import ExerciseProcessEnum
from apps.core.handlers.protocol import RequestDataProtocol

from ..abstract import AbstractRequestValidator
from ..dto import ExerciseActionWebDTO
from ..protocol import ExerciseProcessAction

log = logging.getLogger(__name__)

_RequestData = RequestDataProtocol[ExerciseProcessAction]


class ProcessExerciseWebValidator(
    AbstractRequestValidator[
        _RequestData,
        ExerciseActionWebDTO,
    ],
):
    """Process exercise request WEB validator."""

    def validate(
        self,
        data: _RequestData,
    ) -> ExerciseActionWebDTO:
        """Validate exercise request WEB data."""
        try:
            return ExerciseActionWebDTO(
                action=ExerciseProcessEnum(data.data['action']),
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
