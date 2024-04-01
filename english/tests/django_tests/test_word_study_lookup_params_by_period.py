import datetime
from datetime import timedelta

from django.utils import timezone

from django.test import TestCase
from django.urls import reverse_lazy

from english.models import WordModel
from english.services import create_lookup_params, get_words_for_study
from users.models import UserModel


class TestLookupParametersByPeriod(TestCase):
    """Тест фильтрации слов по периодам изменения.

    Для фильтрации используется поле модели - дата изменения слова.
    Измененное слово должно включаться в выборку слов при фильтрации.
    """

    fixtures = ['english/tests/fixtures/wse-fixtures-3.json']

    TestCase.maxDiff = None

    def setUp(self):
        self.user_id = 3
        user = UserModel.objects.get(pk=self.user_id)
        # Сегодняшняя дата (`<class 'datetime.datetime'>`).
        self.day_today = datetime.datetime.now(tz=timezone.utc)

        # Добавление слов в базу данных.

        # Слово добавлено сегодня (`<class 'english.models.words.WordModel'>`).
        self.word_added_today = WordModel.objects.create(
            user=user,
            words_eng='word today',
            words_rus='слово сегодня',
            word_count='NC',
            created_at=self.day_today,
        )
        # Слово добавлено 3 дня назад.
        self.word_added_3_days_ago = WordModel.objects.create(
            user=user,
            words_eng='word 3 day ago',
            words_rus='слово 3 дня назад',
            word_count='NC',
            created_at=self.day_today - timedelta(days=3),
        )
        # Слово добавлено 3 недели назад
        self.word_added_3_week_ago = WordModel.objects.create(
            user=user,
            words_eng='word 3 weeks ago',
            words_rus='слово 3 недели назад',
            word_count='NC',
            created_at=self.day_today - timedelta(weeks=3),
        )
        # Слово добавлено 5 недель назад.
        self.word_added_5_week_ago = WordModel.objects.create(
            user=user,
            words_eng='word 5 weeks ago',
            words_rus='слово 5 недель назад',
            word_count='NC',
            created_at=self.day_today - timedelta(weeks=5),
        )

        # Дата добавления первого слова (`<class 'datetime.datetime'>`).
        # Используется для задания начала периода фильтрации.
        self.begin_date_period = (
            WordModel.objects.order_by('updated_at').first().updated_at
        )

        # Url выбора параметров поиска для фильтрации слов.
        # `<class 'django.utils.functional.lazy.<locals>.__proxy__'>`
        self.word_study_start_url = reverse_lazy('english:word_study_question')

    def test_filter_period_only_today(self):
        """Тест фильтра слов по периоду "только сегодня".
        """
        querydict = {
            'favorites': False, 'category': '0', 'source': '0',
            'period_start_date': 'DT', 'period_end_date': 'DT',
            'word_count': ['OW', 'CB', 'NC'], 'knowledge_assessment': ['S'],
        }
        params = create_lookup_params(querydict)
        filtered_words = get_words_for_study(params, self.user_id)

        self.assertTrue(filtered_words.contains(self.word_added_today))
        self.assertFalse(filtered_words.contains(self.word_added_3_days_ago))

    def test_filter_period_3_days_ago_till_today(self):
        """Тест фильтра слов по периоду "3 дня назад" до "только сегодня".
        """
        querydict = {
            'favorites': False, 'category': '0', 'source': '0',
            'period_start_date': 'D3', 'period_end_date': 'DT',
            'word_count': [], 'knowledge_assessment': ['S'],
        }
        params = create_lookup_params(querydict)
        filtered_words = get_words_for_study(params, self.user_id)

        self.assertTrue(filtered_words.contains(self.word_added_today))
        self.assertTrue(filtered_words.contains(self.word_added_3_days_ago))
        self.assertFalse(filtered_words.contains(self.word_added_3_week_ago))

    def test_filter_period_4_week_ago_till_1_week_ago(self):
        """Тест фильтра слов по периоду "4 недели назад" до "неделя назад"."""
        querydict = {
            'favorites': False, 'category': '0', 'source': '0',
            'period_start_date': 'W4', 'period_end_date': 'W1',
            'word_count': [], 'knowledge_assessment': ['S'],
        }
        params = create_lookup_params(querydict)
        filtered_words = get_words_for_study(params, self.user_id)

        self.assertTrue(filtered_words.contains(self.word_added_3_week_ago))
        self.assertFalse(filtered_words.contains(self.word_added_3_days_ago))
        self.assertFalse(filtered_words.contains(self.word_added_5_week_ago))

    def test_filter_period_not_choised_till_1_week_ago(self):
        """Тест фильтра слов по периоду "не выбран" до "неделя назад"."""
        querydict = {
            'favorites': False, 'category': '0', 'source': '0',
            'period_start_date': 'NC', 'period_end_date': 'W1',
            'word_count': [], 'knowledge_assessment': ['S'],
        }
        params = create_lookup_params(querydict)
        filtered_words = get_words_for_study(params, self.user_id)

        self.assertTrue(filtered_words.contains(self.word_added_3_week_ago))
        self.assertFalse(filtered_words.contains(self.word_added_3_days_ago))

    def test_filter_period_not_choised_till_today(self):
        """Тест фильтра слов по периоду "не выбран" до "сегодня"."""
        querydict = {
            'favorites': False, 'category': '0', 'source': '0',
            'period_start_date': 'NC', 'period_end_date': 'DT',
            'word_count': [], 'knowledge_assessment': ['S'],
        }
        params = create_lookup_params(querydict)
        filtered_words = get_words_for_study(params, self.user_id)

        self.assertTrue(filtered_words.contains(self.word_added_today)),
        self.assertTrue(filtered_words.contains(self.word_added_5_week_ago))
