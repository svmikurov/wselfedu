"""Web presentation request validator."""

from typing import Any

from apps.core.handlers.protocols import DetailValidator, RegularValidator

from .. import schemas

type RequestData = dict[str, Any]


class WebPresentationValidator(
    RegularValidator[RequestData, schemas.RegularConditionRequest]
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


class WebTestValidator(RegularValidator[RequestData, schemas.TestRequestDTO]):
    """Web request test exercise validator."""

    @classmethod
    def validate(cls, raw_data: RequestData) -> schemas.TestRequestDTO:
        """Validate the web request data."""
        print(f'{raw_data = }')
        return schemas.TestRequestDTO(**raw_data)


class WebAssignedTestValidator(
    DetailValidator[RequestData, schemas.DetailTestRequestDTO]
):
    """Web request assigned test exercise validator."""

    @classmethod
    def validate(
        cls, raw_data: RequestData, pk: int
    ) -> schemas.DetailTestRequestDTO:
        """Validate the web request data."""
        return schemas.DetailTestRequestDTO(**raw_data, pk=pk)
