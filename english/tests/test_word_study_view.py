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


class TestStudyWordsView(TestCase):
    """Тест представлений упражнения изучения слов."""

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        """Set suite up."""
        self.client = Client()
        self.user = UserModel.objects.get(pk=2)

        self.words_choose_url = reverse_lazy('english:words_choose')
        self.start_word_study_url = reverse_lazy('english:start_word_study')
        self.answer_word_study_url = reverse_lazy('english:word_study_answer')
        self.question_word_study_url = reverse_lazy(
            'english:word_study_question'
        )

        self.lookup_parameters = {
            'word_count': ['OW', 'CB', 'NC'],
            'assessment': ['studying', 'repetition']
        }

    def test_word_choose_page_status(self):
        """Test word choose page 200 status.
        """
        response = self.client.get(self.words_choose_url)
        self.assertEqual(response.status_code, 200)

    def test_start_word_study_page_status(self):
        """Test start word study page 302 status.
        """
        self.client.force_login(self.user)
        # Старт выполнения задания.
        # Редирект на формирование задания и отображение вопроса.
        response = self.client.get(
            self.start_word_study_url,
            self.lookup_parameters,
        )
        self.assertRedirects(response, self.question_word_study_url, 302)

    def test_question_word_study_page_status(self):
        """Test question word study page 200 status.
        """
        self.client.force_login(self.user)
        self.client.get(self.start_word_study_url, self.lookup_parameters)

        response = self.client.get(self.question_word_study_url)
        self.assertEqual(response.status_code, 200)

    def test_answer_word_study_page_status(self):
        """Test answer word study page 200 status.
        """
        self.client.force_login(self.user)
        # Сохраним параметры поиска.
        self.client.get(self.start_word_study_url, self.lookup_parameters)
        # Создадим задачу и сохраним ее условия.
        self.client.get(self.question_word_study_url)

        # Перейдем на страницу представления ответа.
        response = self.client.get(self.answer_word_study_url)
        self.assertEqual(response.status_code, 200)
