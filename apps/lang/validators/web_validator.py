"""Web presentation request validator."""

from typing import Any

from apps.core.handlers.protocol import ValidatorProtocol

from ..schemas import (
    DetailTestRequestDTO,
    ParametersSchema,
    RegularConditionRequest,
    SettingsSchema,
    TestRequestDTO,
)


class WebPresentationValidator(ValidatorProtocol[RegularConditionRequest]):
    """Web request presentation validator."""

    @classmethod
    def validate(cls, raw_data: dict[str, Any]) -> RegularConditionRequest:
        """Validate the web request presentation data."""
        return RegularConditionRequest(
            parameters=ParametersSchema(**raw_data),
            settings=SettingsSchema(**raw_data),
        )


class WebTestValidator(ValidatorProtocol[TestRequestDTO]):
    """Web request test exercise validator."""

    @classmethod
    def validate(cls, raw_data: dict[str, Any]) -> TestRequestDTO:
        """Validate the web request data."""
        print(f'{raw_data = }')
        return TestRequestDTO(exercise_status=raw_data.query['status'])


class WebAssignedTestValidator(ValidatorProtocol[DetailTestRequestDTO]):
    """Web request assigned test exercise validator."""

    @classmethod
    def validate(cls, raw_data: dict[str, Any]) -> DetailTestRequestDTO:
        """Validate the web request data."""
        return DetailTestRequestDTO(**raw_data)
