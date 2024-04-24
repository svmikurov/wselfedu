"""Модуль тестирования упражнения Изучение слов.
"""
import datetime
from unittest import skip

from django.test import Client, TestCase
from django.urls import reverse_lazy
from django.utils import timezone

from english.models import WordModel
from users.models import UserModel


class TestChoiceEnglishWordsStudy(TestCase):
    """Протестируй получение параметров пользователя для писка слов."""

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        self.words_choice_url = reverse_lazy('english:word_choice')

    def test_get_words_choice_page(self):
        """Тест статуса страницы выбора параметров поиска слов для изучения."""
        response = self.client.get(self.words_choice_url)
        self.assertEqual(response.status_code, 200)


class TestStudyWordView(TestCase):
    """Тест представлений упражнения изучения слов."""

    fixtures = ['english/tests/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set suite up."""
        self.client = Client()
        self.user = UserModel.objects.get(pk=3)

        self.words_choice_url = reverse_lazy('english:word_choice')
        self.start_study_url = reverse_lazy('english:start_word_study')
        self.answer_url = reverse_lazy('english:word_study_answer')
        self.question_url = reverse_lazy('english:word_study_question')

        self.querydict = {
            'favorites': False, 'category': '0', 'source_id': '0',
            'period_start_date': 'NC', 'period_end_date': 'DT',
            'word_count': ['OW', 'CB', 'NC'], 'knowledge_assessment': ['S'],
        }

        self.begin_date_period = (
            WordModel.objects.order_by('updated_at').first().updated_at
        )
        self.lookup_params = {
            'word_count__in': ['OW', 'CB', 'NC'],
            'created_at__range': (
                self.begin_date_period.strftime(
                    '%Y-%m-%d 00:00:00+00:00'),
                datetime.datetime.now(tz=timezone.utc).strftime(
                    '%Y-%m-%d 23:59:59+00:00'),
            ),
            'worduserknowledgerelation__knowledge_assessment__in': [
                0, 1, 2, 3, 4, 5, 6, 9, 10
            ],
        }

    def test_word_choice_page_status(self):
        """Test word choose page 200 status.
        """
        response = self.client.get(self.words_choice_url)
        self.assertEqual(response.status_code, 200)

    @skip('Update test')
    def test_question_word_study_page_status(self):
        """Test question word study page 200 status.
        """
        self.client.force_login(self.user)

        session = self.client.session
        session['lookup_params'] = self.lookup_params
        session.save()

        response = self.client.get(self.question_url)
        self.assertEqual(response.status_code, 200)

    @skip('Update test')
    def test_answer_word_study_page_status(self):
        """Test answer word study page 200 status.
        """
        self.client.force_login(self.user)
        session = self.client.session
        session['lookup_params'] = self.lookup_params
        session.save()

        self.client.get(self.question_url)
        response = self.client.get(self.answer_url)
        self.assertEqual(response.status_code, 200)
