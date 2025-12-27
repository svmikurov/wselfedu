"""Web presentation request validator tests."""

import pytest
from pydantic import ValidationError

from apps.lang.validators import web_validator

from ....fixtures.lang.no_db.presentation import (
    REQUEST_DTO,
    WEB_REQUEST,
)


class TestValidator:
    """Get presentation request form tests."""

    def test_validate_success(self) -> None:
        """Success validated."""
        # Act & Assert
        validator = web_validator.WebPresentationValidator()
        assert (
            validator.validate(WEB_REQUEST).model_dump()  # type: ignore[arg-type]
            == REQUEST_DTO.model_dump()
        )

    def test_validate_error(self) -> None:
        """Validation error exception raises on validate error."""
        # Act & Assert
        with pytest.raises(ValidationError):
            validator = web_validator.WebPresentationValidator()
            # Category field have `str` type, not `list`
            validator.validate({'category': ['1', '2']})
