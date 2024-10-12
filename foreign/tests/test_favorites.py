"""Test favorites word processing module."""

from django.test import TestCase

from foreign.models import WordFavorites
from foreign.queries import (
    is_word_in_favorites,
    update_word_favorites_status,
)


class TestWordsFavorites(TestCase):
    """Test favorites word processing class."""

    fixtures = ['tests/fixtures/foreign.json', 'tests/fixtures/users.json']

    def setUp(self) -> None:
        """Set up test data."""
        self.user_id = 3
        self.word_id = 3

    def test_is_word_in_favorites(self) -> None:
        """Test the method is word in favorites."""
        self.assertTrue(is_word_in_favorites(self.user_id, self.word_id))

    def test_update_words_favorites_status(self) -> None:
        """Test changing the status of the selected word."""
        self.assertTrue(WordFavorites.objects.filter(user=3, word=3).exists())
        update_word_favorites_status(self.user_id, self.word_id)
        self.assertFalse(WordFavorites.objects.filter(user=3, word=3).exists())
        update_word_favorites_status(self.user_id, self.word_id)
        self.assertTrue(WordFavorites.objects.filter(user=3, word=3).exists())
