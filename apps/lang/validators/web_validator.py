"""Web presentation request validator."""

from typing import Any

from apps.core.handlers.protocol import ResourceValidator, ValidatorProtocol

from .. import schemas

type RequestData = dict[str, Any]


class WebPresentationValidator(
    ValidatorProtocol[RequestData, schemas.RegularConditionRequest]
):
    """Web request presentation validator."""

    @classmethod
    def validate(
        cls, raw_data: RequestData
    ) -> schemas.RegularConditionRequest:
        """Validate the web request presentation data."""
        return schemas.RegularConditionRequest(
            parameters=schemas.ParametersSchema(**raw_data),
            settings=schemas.SettingsSchema(**raw_data),
        )


class WebTestValidator(ValidatorProtocol[RequestData, schemas.TestRequestDTO]):
    """Web request test exercise validator."""

    @classmethod
    def validate(cls, raw_data: RequestData) -> schemas.TestRequestDTO:
        """Validate the web request data."""
        return schemas.TestRequestDTO(**raw_data)


class WebAssignedTestValidator(
    ResourceValidator[RequestData, schemas.DetailTestRequestDTO]
):
    """Web request assigned test exercise validator."""

    @classmethod
    def validate(
        cls, raw_data: RequestData, pk: int
    ) -> schemas.DetailTestRequestDTO:
        """Validate the web request data."""
        return schemas.DetailTestRequestDTO(**raw_data, pk=pk)
