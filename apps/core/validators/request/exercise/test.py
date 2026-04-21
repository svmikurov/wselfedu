"""Test exercise validator."""

import logging
from typing import TypeAlias

from apps.core.contracts.request.protocol import HasAction
from apps.core.contracts.request.web.exercise import CreateExerciseRequestDTO
from apps.core.domains.exercise.enums import ExerciseProcessEnum
from apps.core.handlers.protocol import RequestDataProtocol

from ..abstract import AbstractRequestValidator
from ..protocol import ExerciseProcessAction

log = logging.getLogger(__name__)

DataT: TypeAlias = RequestDataProtocol[ExerciseProcessAction]
ValidatedT: TypeAlias = HasAction[ExerciseProcessEnum]


class WebTestExerciseValidator(
    AbstractRequestValidator[DataT, ValidatedT],
):
    """Test exercise answer web data validator."""

    def validate(self, data: DataT) -> ValidatedT:
        """Validate test exercise user's answer data."""
        try:
            return CreateExerciseRequestDTO(
                action=ExerciseProcessEnum(data.data['action']),
            )
        except Exception as exc:
            log.error(f'Unexpected validation error: {exc}')
            raise
