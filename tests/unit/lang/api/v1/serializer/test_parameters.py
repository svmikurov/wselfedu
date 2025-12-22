"""Word study Presentation parameter Serializer tests."""

from apps.lang.api.v1.serializers import study as serializers
from tests.fixtures.lang.no_db import translations as fixtures


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


class TestToPython:
    """Presentation case API data convert to python."""

    def test_to_python(self) -> None:
        """Convert API data to python."""
        serializer = serializers.StudyParametersSerializer(
            data=fixtures.TRANSLATION_CASE_PARAMETERS
        )
        serializer.is_valid()

        assert (
            serializer.data == fixtures.TRANSLATION_CASE_PARAMETERS_TO_PYTHON
        )
