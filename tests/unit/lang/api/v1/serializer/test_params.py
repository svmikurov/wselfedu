"""Word study Presentation parameter Serializer tests."""

from apps.lang.api.v1.serializers import study as serializers
from tests.fixtures.lang.no_db import word_study_params as fixtures


class TestSerializer:
    """Word study Presentation parameter Serializer tests."""

    def test_valid_data(self) -> None:
        """Test the valid data serialization."""
        serializer = serializers.SetParametersSerializer(
            data=fixtures.PRESENTATION_PARAMETERS
        )
        assert serializer.is_valid()

    def test_empty_data(self) -> None:
        """Test the valid data serialization."""
        serializer = serializers.SetParametersSerializer(data={})
        assert not serializer.is_valid()
