"""Модуль тестирования упражнения Изучение слов.
"""

from django.test import TestCase
from django.urls import reverse_lazy


class TestChooseEnglishWordsStudy(TestCase):
    """Протестируй применение параметров пользователя для писка слов."""

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        self.words_choose_url = reverse_lazy('english:words_choose')

    def test_get_words_choose_page(self):
        """Тест статуса страницы выбора параметров поиска слов для изучения."""
        response = self.client.get(self.words_choose_url)
        self.assertTrue(response.status_code, 200)
