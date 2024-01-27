"""Модуль тестирования упражнения Изучение слов.
"""

from django.test import TestCase
from django.urls import reverse_lazy

from english.tasks.study_words import filter_words
from users.models import UserModel


class TestChooseEnglishWordsStudy(TestCase):
    """Протестируй применение параметров пользователя для писка слов."""

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        user_id = UserModel.objects.get(username='user1').pk
        self.words_choose_url = reverse_lazy('eng:words_choose')
        self.study_words_url = reverse_lazy(
            'eng:repetition', kwargs={'task_status': 'start'},
        )

        # Параметры пользователя поиска слов для изучения.
        level = {0, 1, 2, 3, 4}
        count = ('OW', 'NC')
        category_id = 2,
        source_id = 2,
        self.lookup_parameters = {
            'favorites__pk': user_id,
            'category_id': category_id,
            'source_id': source_id,
            'word_count__in': count,
            'worduserknowledgerelation__knowledge_assessment__in': level,
            'worduserknowledgerelation__user_id': user_id,
        }
        self.lookup_result = {'word02', 'word06'}

    def test_get_words_choose_page(self):
        """Тест статуса страницы выбора параметров поиска слов для изучения."""
        response = self.client.get(self.words_choose_url)
        self.assertTrue(response.status_code, 200)

    def test_filter_words(self):
        """Тест фильтра слов по всем параметрам поиска."""
        filtered_words = filter_words(self.lookup_parameters)
        received_words_eng = filtered_words.values_list('words_eng', flat=True)
        self.assertEqual(set(received_words_eng), self.lookup_result)
