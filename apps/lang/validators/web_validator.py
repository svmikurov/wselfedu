"""Web presentation request validator."""

from typing import Any

from apps.core.handlers.protocol import ValidatorProtocol

from ..schemas import (  # type: ignore
    DetailTestRequestDTO,
    ExerciseParametersDTO,
    ParametersSchema,
    SettingsSchema,
    TestRequestDTO,
)


class WebPresentationValidator(ValidatorProtocol[ExerciseParametersDTO]):  # type: ignore
    """Web request presentation validator."""

    @classmethod
    def validate(cls, raw_data: dict[str, Any]) -> ExerciseParametersDTO:
        """Validate the web request presentation data."""
        return ExerciseParametersDTO(
            parameters=ParametersSchema(**raw_data),
            conf=SettingsSchema(**raw_data),
        )


class WebTestValidator(ValidatorProtocol[TestRequestDTO]):  # type: ignore
    """Web request test exercise validator."""

    @classmethod
    def validate(cls, raw_data: dict[str, Any]) -> TestRequestDTO:
        """Validate the web request data."""
        return TestRequestDTO(exercise_status=raw_data.query['status'])  # type: ignore


class WebAssignedTestValidator(ValidatorProtocol[DetailTestRequestDTO]):  # type: ignore
    """Web request assigned test exercise validator."""

    @classmethod
    def validate(cls, raw_data: dict[str, Any]) -> DetailTestRequestDTO:
        """Validate the web request data."""
        return DetailTestRequestDTO(**raw_data)
