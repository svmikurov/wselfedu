"""Модуль тестирования упражнения Изучение слов.
"""
from django.test import Client, TestCase
from django.urls import reverse_lazy

from users.models import UserModel


class TestChooseEnglishWordsStudy(TestCase):
    """Протестируй получение параметров пользователя для писка слов."""

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        self.words_choose_url = reverse_lazy('english:words_choose')

    def test_get_words_choose_page(self):
        """Тест статуса страницы выбора параметров поиска слов для изучения."""
        response = self.client.get(self.words_choose_url)
        self.assertEqual(response.status_code, 200)


class TestStudyEnglishWordsView(TestCase):
    """Тест упражнения изучения слов."""

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        """Set suite up."""
        self.client = Client()
        self.user = UserModel.objects.get(pk=2)
        self.words_choose_url = reverse_lazy('english:words_choose')
        self.start_words_study_url = reverse_lazy(
            'english:words_study', kwargs={'task_status': 'start'}
        )
        self.answer_words_study_url = reverse_lazy(
            'english:words_study', kwargs={'task_status': 'answer'}
        )

    def test_words_choose_page_status(self):
        """Test words choose page 200 status.
        """
        response = self.client.get(self.words_choose_url)
        self.assertEqual(response.status_code, 200)

    def test_start_words_study_page_status(self):
        """Test start words study page 200 status.
        """
        response = self.client.get(self.start_words_study_url)
        self.assertEqual(response.status_code, 200)

    def test_answer_words_study_page_status(self):
        """Test answer words study page 200 status."""
        lookup_parameters = {
            'word_count': ['OW', 'CB', 'NC'],
            'assessment': ['studying', 'repetition']
        }
        self.client.force_login(self.user)
        # Старт выполнения задания, формируется задача, сохраняется задача.
        self.client.get(self.start_words_study_url, lookup_parameters)
        # Выполняется задание, есть сформированная задача.
        # Становится возможным переход на статус 'answer'.
        # Без старта, без сохранения задачи тест выдаст ошибку!
        response = self.client.get(self.answer_words_study_url)
        self.assertEqual(response.status_code, 200)
