import datetime

from django.utils import timezone

from django.test import TestCase
from django.urls import reverse_lazy

from english.models import WordModel
from english.services import (
    create_lookup_params,
    get_words_for_study,
)
from users.models import UserModel


class TestKnowledgeAssessmentLookupParameter(TestCase):
    """Тест получения из request параметров поиска слов для задачи.
    """

    fixtures = ['english/tests/fixtures/wse-fixtures-3.json']

    def setUp(self):
        self.objects = WordModel.objects
        self.user_id = 3
        self.user = UserModel.objects.get(pk=self.user_id)
        self.querydict = {
            'favorites': True, 'category': 0, 'source': 0,
            'period_start_date': 'NC', 'period_end_date': 'DT',
            'word_count': ['OW', 'CB', 'NC'],
            'knowledge_assessment': ['S', 'E'],
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

        self.word_id_study = 4
        self.word_id_repetition = 5
        self.word_id_examination = 7
        self.user_word_id_know = 9

        # Url выбора параметров поиска для фильтрации слов.
        self.word_study_start_url = reverse_lazy('english:word_study_question')

    def _is_contain(self, queryset, word_id):
        """Check is QuerySet contain specific word."""
        return queryset.contains(self.objects.get(id=word_id))

    def test_get_studying_words(self):
        """Протестируй фильтрацию слов по knowledge_assessment studying."""
        querydict = {
            'favorites': False, 'category': 0, 'source': 0,
            'period_start_date': 'NC', 'period_end_date': 'DT',
            'word_count': ['OW', 'CB', 'NC'], 'knowledge_assessment': ['S'],
        }
        lookup_parameters = create_lookup_params(querydict)
        words = get_words_for_study(lookup_parameters, self.user_id)

        self.assertTrue(self._is_contain(words, self.word_id_study))
        self.assertFalse(self._is_contain(words, self.word_id_repetition))
        self.assertFalse(self._is_contain(words, self.word_id_examination))
        self.assertFalse(self._is_contain(words, self.user_word_id_know))

    def test_get_repetition_words(self):
        """Протестируй фильтрацию слов по knowledge_assessment repetition."""
        querydict = {
            'favorites': False, 'category': 0, 'source': 0,
            'period_start_date': 'NC', 'period_end_date': 'DT',
            'word_count': ['OW', 'CB', 'NC'], 'knowledge_assessment': ['R'],
        }
        lookup_parameters = create_lookup_params(querydict)
        words = get_words_for_study(lookup_parameters, self.user_id)

        self.assertFalse(self._is_contain(words, self.word_id_study))
        self.assertTrue(self._is_contain(words, self.word_id_repetition))
        self.assertFalse(self._is_contain(words, self.word_id_examination))
        self.assertFalse(self._is_contain(words, self.user_word_id_know))

    def test_get_examination_words(self):
        """Протестируй фильтрацию слов по knowledge_assessment examination."""
        querydict = {
            'favorites': False, 'category': 0, 'source': 0,
            'period_start_date': 'NC', 'period_end_date': 'DT',
            'word_count': ['PS'], 'knowledge_assessment': ['E'],
        }
        lookup_parameters = create_lookup_params(querydict, self.user_id)
        words = get_words_for_study(lookup_parameters, self.user_id)

        self.assertFalse(self._is_contain(words, self.word_id_study))
        self.assertFalse(self._is_contain(words, self.word_id_repetition))
        self.assertTrue(self._is_contain(words, self.word_id_examination))
        self.assertFalse(self._is_contain(words, self.user_word_id_know))

    def test_get_know_words(self):
        """Протестируй фильтрацию слов по knowledge_assessment learned."""
        querydict = {
            'favorites': False, 'category': 0, 'source': 0,
            'period_start_date': 'NC', 'period_end_date': 'DT',
            'word_count': ['OW', 'CB', 'NC'], 'knowledge_assessment': ['K'],
        }
        lookup_parameters = create_lookup_params(querydict, self.user_id)
        words = get_words_for_study(lookup_parameters, self.user_id)

        self.assertFalse(self._is_contain(words, self.word_id_study))
        self.assertFalse(self._is_contain(words, self.word_id_repetition))
        self.assertFalse(self._is_contain(words, self.word_id_examination))
        self.assertTrue(self._is_contain(words, self.user_word_id_know))

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
            'worduserknowledgerelation__knowledge_assessment__in': [*range(7)]
        }

        words = get_words_for_study(params, self.user_id)
        self.assertTrue(words.contains(new_word))

    def test_knowledge_assessment_by_users(self):
        """Тест фильтра слов по knowledge_assessment конкретного пользователя
        в функции get_words_for_study.

        Модель m2m.
        Значение knowledge_assessment слов других пользователей не должно
        учитываться при фильтрации слов для текущего пользователя.

        Check that the QuerySet contains the specified words.
        """
        params = {
            'word_count__in': ['OW', 'CB', 'NC'],
            'worduserknowledgerelation__knowledge_assessment__in': [*range(7)]
        }
        words = get_words_for_study(params, self.user_id)

        word_id_study_another_user = 13
        word_id_repetition_another_user = 16

        self.assertTrue(self._is_contain(words, self.word_id_study))
        self.assertFalse(self._is_contain(words, self.word_id_repetition))
        self.assertFalse(self._is_contain(words, word_id_study_another_user))
        self.assertFalse(self._is_contain(
            words, word_id_repetition_another_user
        ))
