import datetime

from django.utils import timezone

from django.test import TestCase
from django.urls import reverse_lazy

from english.models import WordModel
from english.services import (
    create_lookup_params,
    get_random_query_from_queryset,
    get_words_for_study,
)
from english.tasks.study_words import shuffle_sequence
from users.models import UserModel


class TestKnowledgeAssessmentLookupParameter(TestCase):
    """Тест получения из request параметров поиска слов для задачи.
    """

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        self.objects = WordModel.objects
        self.user_id = 2
        self.user = UserModel.objects.get(pk=self.user_id)
        self.querydict = {
            'favorites': True, 'category': 0, 'source': 0,
            'period_start_date': 'NC', 'period_end_date': 'DT',
            'word_count': ['OW', 'CB', 'NC'],
            'knowledge_assessment': ['L', 'E'],
        }

        self.begin_date_period = (
            WordModel.objects.order_by('updated_at').first().updated_at
        )
        # В word_count__in программно добавляется 'NC'.
        self.params = {
            'favorites__pk': 2,
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

        # Url выбора параметров поиска для фильтрации слов.
        self.word_study_start_url = reverse_lazy('english:word_study_question')

    def test_get_studying_words(self):
        """Протестируй фильтрацию слов по knowledge_assessment studying."""
        querydict = {
            'favorites': False, 'category': 0, 'source': 0,
            'period_start_date': 'NC', 'period_end_date': 'DT',
            'word_count': ['OW', 'CB', 'NC'], 'knowledge_assessment': ['L'],
        }
        lookup_parameters = create_lookup_params(querydict)
        words = get_words_for_study(lookup_parameters, self.user_id)

        self.assertTrue(words.contains(self.objects.get(id=1)))
        self.assertTrue(words.contains(self.objects.get(id=2)))
        self.assertFalse(words.contains(self.objects.get(id=3)))
        self.assertTrue(words.contains(self.objects.get(id=6)))

    def test_get_repetition_words(self):
        """Протестируй фильтрацию слов по knowledge_assessment repetition."""
        querydict = {
            'favorites': False, 'category': 0, 'source': 0,
            'period_start_date': 'NC', 'period_end_date': 'DT',
            'word_count': ['OW', 'CB', 'NC'], 'knowledge_assessment': ['R'],
        }
        lookup_parameters = create_lookup_params(querydict)
        words = get_words_for_study(lookup_parameters, self.user_id)

        self.assertFalse(words.contains(self.objects.get(id=2)))
        self.assertTrue(words.contains(self.objects.get(id=3)))
        self.assertFalse(words.contains(self.objects.get(id=4)))
        self.assertFalse(words.contains(self.objects.get(id=5)))

    def test_get_examination_words(self):
        """Протестируй фильтрацию слов по knowledge_assessment examination."""
        querydict = {
            'favorites': False, 'category': 0, 'source': 0,
            'period_start_date': 'NC', 'period_end_date': 'DT',
            'word_count': ['PS'], 'knowledge_assessment': ['E'],
        }
        lookup_parameters = create_lookup_params(querydict, self.user_id)
        words = get_words_for_study(lookup_parameters, self.user_id)

        self.assertFalse(words.contains(self.objects.get(id=2)))
        self.assertFalse(words.contains(self.objects.get(id=3)))
        self.assertTrue(words.contains(self.objects.get(id=4)))
        self.assertFalse(words.contains(self.objects.get(id=5)))

    def test_get_learned_words(self):
        """Протестируй фильтрацию слов по knowledge_assessment learned."""
        querydict = {
            'favorites': False, 'category': 0, 'source': 0,
            'period_start_date': 'NC', 'period_end_date': 'DT',
            'word_count': ['OW', 'CB', 'NC'], 'knowledge_assessment': ['L'],
        }
        lookup_parameters = create_lookup_params(querydict, self.user_id)
        words = get_words_for_study(lookup_parameters, self.user_id)

        self.assertTrue(words.contains(self.objects.get(id=2)))
        self.assertFalse(words.contains(self.objects.get(id=3)))
        self.assertFalse(words.contains(self.objects.get(id=4)))
        self.assertFalse(words.contains(self.objects.get(id=5)))

    def test_add_to_lookup_parameters_new_words(self):
        """Тест включить в фильтр слова, еще не имеющие оценку уровня знания.
        """
        new_word = WordModel.objects.create(
            user=self.user,
            words_eng='new word',
            words_rus='новое слово',
            word_count='OW',
            updated_at='2024-01-14 04:35:37+00:00',
        )
        params = {
            'word_count__in': ['OW', 'CB', 'NC'],
            'created_at__range': (
                self.begin_date_period.strftime(
                    '%Y-%m-%d 00:00:00+00:00'
                ),
                datetime.datetime.now(tz=timezone.utc).strftime(
                    '%Y-%m-%d 23:59:59+00:00'
                ),
            ),
            'worduserknowledgerelation__knowledge_assessment__in': [
                0, 1, 2, 3, 4, 5, 6,
            ]
        }

        words = get_words_for_study(params, self.user_id)
        self.assertTrue(words.contains(new_word))

    def test_knowledge_assessment_by_users(self):
        """Тест фильтра слов по knowledge_assessment конкретного пользователя
        в функции get_words_for_study.

        Модель m2m.
        Значение knowledge_assessment слов других пользователей не должно
        учитываться при фильтрации слов для текущего пользователя.
        """
        params = {
            'word_count__in': ['OW', 'CB', 'NC'],
            'worduserknowledgerelation__knowledge_assessment__in': [
                0, 1, 2, 3, 4, 5, 6
            ]
        }

        words = get_words_for_study(params, self.user_id)

        self.assertTrue(words.contains(self.objects.get(id=1)))
        self.assertTrue(words.contains(self.objects.get(id=2)))
        self.assertFalse(words.contains(self.objects.get(id=3)))
        self.assertTrue(words.contains(self.objects.get(id=6)))
