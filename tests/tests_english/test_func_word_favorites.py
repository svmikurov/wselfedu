from django.test import TestCase

from english.models import WordsFavoritesModel
from english.orm_queries import (
    is_word_in_favorites,
    update_word_favorites_status,
)


class TestWordsFavorites(TestCase):
    fixtures = ['tests/tests_english/fixtures/wse-fixtures.json']

    def setUp(self):
        # Атрибуты создания связи об избранном слове.
        self.user_id = 1
        self.word_id = 2
        # Атрибуты существующей в фикстуре связи об избранном слове.
        self.user_id_in_favorites = 2
        self.word_id_in_favorites = 1

    def test_is_word_in_favorites(self):
        """Протестируй is_word_in_favorites()."""
        self.assertTrue(
            is_word_in_favorites(
                self.user_id_in_favorites, self.word_id_in_favorites
            )
        )

    def test_update_words_favorites_status(self):
        """Протестируй изменение статуса избранного слова."""
        user_id = 1
        word_id = 2

        self.assertTrue(
            WordsFavoritesModel.objects.filter(user=1, word=2).exists()
        )
        update_word_favorites_status(word_id=word_id, user_id=user_id)
        self.assertFalse(
            WordsFavoritesModel.objects.filter(user=1, word=2).exists()
        )
        update_word_favorites_status(word_id=word_id, user_id=user_id)
        self.assertTrue(
            WordsFavoritesModel.objects.filter(user=1, word=2).exists()
        )
