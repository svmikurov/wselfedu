"""Web presentation request validator."""

from typing import Any

from .. import schemas
from ..types import presentation


class WebPresentationValidator(
    presentation.Validator[dict[str, Any], schemas.PresentationRequest]
):
    """Web request presentation validator."""

    @classmethod
    def validate(cls, raw_data: dict[str, Any]) -> schemas.PresentationRequest:
        """Validate the web request presentation data."""
        return schemas.PresentationRequest(
            parameters=schemas.ParametersSchema(**raw_data),
            settings=schemas.SettingsSchema(**raw_data),
        )
