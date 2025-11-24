"""Word study Presentation parameter Serializer tests."""

from apps.lang import types
from apps.lang.api.v1.serializers.study import (
    WordStudyPresentationParamsSerializer,
)


class TestSerializer:
    """Word study Presentation parameter Serializer tests."""

    def test_valid_data(
        self,
        word_presentation_params: types.WordPresentationParamsT,
    ) -> None:
        """Test the valid data serialization."""
        serializer = WordStudyPresentationParamsSerializer(
            data=word_presentation_params
        )
        assert serializer.is_valid()

    def test_empty_data(self) -> None:
        """Test the valid data serialization."""
        serializer = WordStudyPresentationParamsSerializer(data={})
        assert not serializer.is_valid()
