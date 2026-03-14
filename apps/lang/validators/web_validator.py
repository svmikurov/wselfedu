"""Web presentation request validator."""

from apps.core.handlers.dto import RequestData
from apps.core.handlers.protocol import (
    ResourceValidatorProtocol,
    ValidatorProtocol,
)

from .. import schemas


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
            parameters=schemas.ParametersSchema(**raw_data.query),
            settings=schemas.SettingsSchema(**raw_data),
        )


class WebTestValidator(ValidatorProtocol[RequestData, schemas.TestRequestDTO]):
    """Web request test exercise validator."""

    @classmethod
    def validate(cls, raw_data: RequestData) -> schemas.TestRequestDTO:
        """Validate the web request data."""
        return schemas.TestRequestDTO(**raw_data.query)


class WebAssignedTestValidator(
    ResourceValidatorProtocol[RequestData, schemas.DetailTestRequestDTO]
):
    """Web request assigned test exercise validator."""

    @classmethod
    def validate(
        cls, raw_data: RequestData, pk: int
    ) -> schemas.DetailTestRequestDTO:
        """Validate the web request data."""
        return schemas.DetailTestRequestDTO(**raw_data, pk=pk)
