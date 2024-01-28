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


class TestStudyEnglishWordsView(TestCase):
    """Тест упражнения изучения слов."""

    def setUp(self):
        self.url = reverse_lazy(
            'english:words_study', kwargs={'task_status': 'start'}
        )
        self.extra_arguments = {'category_id': 1}

    def test_page_status(self):
        response = self.client.get(self.url, self.extra_arguments)
        self.assertEqual(response.status_code, 200)

    def test_get_lookup_parameters(self):
        ...
