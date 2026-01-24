"""Web presentation request validator."""

from typing import Any

from .. import schemas, types

type RequestData = dict[str, Any]


class WebPresentationValidator(
    types.Validator[RequestData, schemas.PresentationRequest]
):
    """Web request presentation validator."""

    @classmethod
    def validate(cls, raw_data: RequestData) -> schemas.PresentationRequest:
        """Validate the web request presentation data."""
        return schemas.PresentationRequest(
            parameters=schemas.ParametersSchema(**raw_data),
            settings=schemas.SettingsSchema(**raw_data),
        )


class WebTestValidator(types.Validator[RequestData, schemas.TestRequestDTO]):
    """Web request test validator."""

    @classmethod
    def validate(cls, raw_data: RequestData) -> schemas.TestRequestDTO:
        """Validate the web request data."""
        return schemas.TestRequestDTO(**raw_data)


class WebAssignedExerciseValidator(
    types.DetailValidator[RequestData, schemas.DetailTestRequestDTO]
):
    """Web request test validator with additional named args."""

    @classmethod
    def validate(
        cls, raw_data: RequestData, pk: int
    ) -> schemas.DetailTestRequestDTO:
        """Validate the web request data."""
        return schemas.DetailTestRequestDTO(**raw_data, pk=pk)
