"""Test exercise validator."""

from apps.core.handlers.protocol import ValidatedDataProtocol
from apps.core.validators.request.dto import TestExerciseAnswerDTO

from .abstract import AbstractRequestValidator
from .protocol import TestExerciseAnswerProtocol, TestExerciseAnswerRequestData


class TestExerciseWebValidator(
    AbstractRequestValidator[
        ValidatedDataProtocol[TestExerciseAnswerRequestData],
        TestExerciseAnswerProtocol,
    ]
):
    """Test exercise answer web data validator."""

    def validate(
        self,
        data: ValidatedDataProtocol[TestExerciseAnswerRequestData],
    ) -> TestExerciseAnswerProtocol:
        """Validate test exercise user's answer data."""
        return TestExerciseAnswerDTO(
            option_value=int(data.data['option_value']),
        )
