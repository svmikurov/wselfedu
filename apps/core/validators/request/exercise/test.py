"""Test exercise validator."""

import logging

from apps.core.domains.exercise.enums import ExerciseProcessEnum
from apps.core.handlers.protocol import RequestDataProtocol
from apps.core.validators.request.dto import ProcessExerciseWebDTO

from ..abstract import AbstractRequestValidator
from ..protocol import (
    OptionAnswerWebData,
    TestExerciseAnswerProtocol,
)

log = logging.getLogger(__name__)


class TestExerciseWebValidator(
    AbstractRequestValidator[
        RequestDataProtocol[OptionAnswerWebData],
        TestExerciseAnswerProtocol,
    ]
):
    """Test exercise answer web data validator."""

    def validate(
        self,
        data: RequestDataProtocol[OptionAnswerWebData],
    ) -> TestExerciseAnswerProtocol:
        """Validate test exercise user's answer data."""
        try:
            return ProcessExerciseWebDTO(
                action=ExerciseProcessEnum(data.data['action']),
                option_value=int(data.data['option_value']),
            )
        except Exception as exc:
            log.error(f'Unexpected validation error: {exc}')
            raise
