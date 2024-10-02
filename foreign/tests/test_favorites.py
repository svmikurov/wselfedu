"""Test favorites word processing module."""

from django.test import TestCase

from foreign.models import WordFavorites
from foreign.queries import (
    is_word_in_favorites,
    update_word_favorites_status,
)


class TestWordsFavorites(TestCase):
    """Test favorites word processing class."""

    fixtures = ['foreign/tests/fixtures/wse-fixtures.json']

    def setUp(self) -> None:
        """Set up test data."""
        self.user_id = 1
        self.word_id = 2
        self.user_id_in_favorites = 2
        self.word_id_in_favorites = 1

    def test_is_word_in_favorites(self) -> None:
        """Протестируй is_word_in_favorites()."""
        self.assertTrue(
            is_word_in_favorites(
                self.user_id_in_favorites, self.word_id_in_favorites
            )
        )

    def test_update_words_favorites_status(self) -> None:
        """Протестируй изменение статуса избранного слова."""
        user_id = 1
        word_id = 2

        self.assertTrue(WordFavorites.objects.filter(user=1, word=2).exists())
        update_word_favorites_status(word_id=word_id, user_id=user_id)
        self.assertFalse(WordFavorites.objects.filter(user=1, word=2).exists())
        update_word_favorites_status(word_id=word_id, user_id=user_id)
        self.assertTrue(WordFavorites.objects.filter(user=1, word=2).exists())
