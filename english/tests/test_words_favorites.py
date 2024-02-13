from django.test import TestCase

from english.models import WordModel, WordsFavoritesModel
from english.services.words_favorites import (
    add_word_to_favorites,
    remove_word_from_favorites,
    is_word_in_favorites, update_words_favorites_status,
)
from users.models import UserModel


class TestWordsFavorites(TestCase):

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        # Атрибуты создания связи об избранном слове.
        self.user_id = 1
        self.word_id = 2
        # Атрибуты существующей в фикстуре связи об избранном слове.
        self.user_id_in_favorites = 2
        self.word_id_in_favorites = 1

    def test_add_word_to_favorites(self):
        """Протестируй добавление слова в список избранных пользователя."""
        # Добавь слово через тест функции.
        add_word_to_favorites(self.user_id, self.word_id)
        # Проверь, есть ли в базе данных добавленная связь.
        self.assertTrue(
            WordsFavoritesModel.objects.filter(
                user=UserModel.objects.get(pk=self.user_id),
                word=WordModel.objects.get(pk=self.word_id),
            ).exists()
        )

    def test_is_word_in_favorites(self):
        """Протестируй is_word_in_favorites()."""
        self.assertTrue(is_word_in_favorites(
            self.user_id_in_favorites, self.word_id_in_favorites
        ))

    def test_remove_word_from_favorites(self):
        """Протестируй удаление слова из списка избранных пользователя."""
        remove_word_from_favorites(
            self.user_id_in_favorites, self.word_id_in_favorites
        )
        self.assertFalse(
            WordsFavoritesModel.objects.filter(
                user=UserModel.objects.get(pk=self.user_id_in_favorites),
                word=WordModel.objects.get(pk=self.word_id_in_favorites),
            ).exists()
        )

    def test_update_words_favorites_status(self):
        """Протестируй изменение статуса избранного слова."""
        user_id = 1
        word_id = 2

        self.assertTrue(
            WordsFavoritesModel.objects.filter(user=1, word=2).exists()
        )
        update_words_favorites_status(word_id, user_id, 'remove')
        self.assertFalse(
            WordsFavoritesModel.objects.filter(user=1, word=2).exists()
        )
