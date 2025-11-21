"""Word study Presentation parameter Serializer tests."""

from apps.lang import types
from apps.lang.api.v1.serializers.study import (
    WordStudyPresentationParamsSerializer,
)

VALID_DATA: types.WordPresentationParamsT = {
    'categories': [{'id': 1, 'name': 'cat 1'}, {'id': 2, 'name': 'cat 2'}],
    'marks': [{'id': 1, 'name': 'mark 1'}],
    'category': {'id': 1, 'name': 'cat 1'},
    'mark': {'id': 1, 'name': 'mark 1'},
    'word_source': {'id': 1, 'name': 'source 1'},
    'order': 'to_native',
    'start_period': {'id': 3, 'name': 'one_week_before'},
    'end_period': None,
    'word_count': 80,
    'question_timeout': 1.5,
    'answer_timeout': 2.0,
}


class TestSerializer:
    """Word study Presentation parameter Serializer tests."""

    def test_valid_data(self) -> None:
        """Test the valid data serialization."""
        serializer = WordStudyPresentationParamsSerializer(data=VALID_DATA)
        assert serializer.is_valid()

    def test_empty_data(self) -> None:
        """Test the valid data serialization."""
        serializer = WordStudyPresentationParamsSerializer(data={})
        assert not serializer.is_valid()
