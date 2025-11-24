"""Word study Presentation parameter Serializer tests."""

from apps.lang import types
from apps.lang.api.v1.serializers.study import (
    WordStudyPresentationParamsSerializer,
)

# TODO: Replace with 'options', 'selected', 'settings' fixtures?
# Union 'options', 'selected', 'settings' fixtures to one?
VALID_DATA: types.WordPresentationParamsT = {
    # Parameter options
    'categories': [{'id': 1, 'name': 'cat 1'}, {'id': 2, 'name': 'cat 2'}],
    'marks': [{'id': 1, 'name': 'mark 1'}],
    'sources': [{'id': 1, 'name': 'mark 1'}],
    'periods': [{'id': 1, 'name': 'today'}, {'id': 2, 'name': 'week_before'}],
    'orders': [
        {'code': 'to_native', 'name': 'На родной'},
        {'code': 'from_native', 'name': 'С родного'},
        {'code': 'random', 'name': 'Случайные'},
    ],
    # Selected parameter
    'category': {'id': 1, 'name': 'cat 1'},
    'mark': {'id': 1, 'name': 'mark 1'},
    'word_source': {'id': 1, 'name': 'source 1'},
    'order': {'code': 'to_native', 'name': 'На родной'},
    'start_period': {'id': 2, 'name': 'week_before'},
    'end_period': {'id': 1, 'name': 'today'},
    # Set parameter
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
