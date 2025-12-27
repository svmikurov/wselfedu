"""Web presentation request validator tests."""

import pytest
from rest_framework.exceptions import ValidationError as DRFValidationError

from apps.lang.validators import api_validator

from ....fixtures.lang.no_db.presentation import API_REQUEST, REQUEST_DTO


class TestValidator:
    """Get presentation request form tests."""

    def test_validate_success(self) -> None:
        """Success validated."""
        # Act
        validator = api_validator.ApiPresentationValidator()

        # Assert
        assert validator.validate(API_REQUEST) == REQUEST_DTO  # type: ignore[arg-type]

    def test_validate_error(self) -> None:
        """Validation error exception raises on validate error."""
        # Act & Assert
        with pytest.raises(DRFValidationError):
            validator = api_validator.ApiPresentationValidator()
            validator.validate({})


class TestSerializer:
    """Get presentation request serializer tests."""

    def test_valid_data(self) -> None:
        """Test the valid data serialization."""
        # Act & Assert
        serializer = api_validator.PresentationSerializer(data=API_REQUEST)
        assert serializer.is_valid(), f'Serializer errors: {serializer.errors}'

    def test_empty_data(self) -> None:
        """Test the valid data serialization."""
        # Act & Assert
        serializer = api_validator.PresentationSerializer(data={})
        assert not serializer.is_valid(), f'Serializer errors: {
            serializer.errors
        }'
