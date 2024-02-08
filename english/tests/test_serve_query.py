"""Тест модуля test_serve_query.py
"""

import datetime
from datetime import timedelta

from django.db.models import Subquery
from django.utils import timezone

from django.test import Client, TestCase
from django.urls import reverse_lazy

from english.models import WordModel, WordUserKnowledgeRelation
from english.services.serve_query import (
    get_random_query_from_queryset,
    create_lookup_parameters,
)
from english.tasks.study_words import shuffle_sequence


class TestLookupParametersByPeriods(TestCase):
    """Тест получения параметра выбора слова по дате добавления слова.

    Для фильтрации используется поле модели - дата изменения слова.
    Измененное слово должно включаться в выборку слов при фильтрации.
    """

    # periods_choices = {
    #     1: 'Сегодня',
    #     2: 'Три дня назад',
    #     3: 'Неделя назад',
    #     4: 'Четыре недели назад',
    #     9: 'Начало не выбрано'
    #     }

    TestCase.maxDiff = None

    def setUp(self):
        self.client = Client()

        # Сегодняшняя дата (`<class 'datetime.datetime'>`).
        self.day_today = datetime.datetime.now(tz=timezone.utc)

        # Добавление слов в базу данных.

        # Слово добавлено сегодня (`<class 'english.models.words.WordModel'>`).
        self.word_added_today = WordModel.objects.create(
            words_eng='word today', words_rus='слово сегодня',
            updated_at=self.day_today,
        )
        # Слово добавлено 3 дня назад.
        self.word_added_3_days_ago = WordModel.objects.create(
            words_eng='word 3 day ago', words_rus='слово 3 дня назад',
            updated_at=self.day_today - timedelta(days=3),
        )
        # Слово добавлено 3 недели назад
        self.word_added_3_week_ago = WordModel.objects.create(
            words_eng='word 3 weeks ago', words_rus='слово 3 недели назад',
            updated_at=self.day_today - timedelta(weeks=3),
        )
        # Слово добавлено 5 недель назад.
        self.word_added_5_week_ago = WordModel.objects.create(
            words_eng='word 5 weeks ago', words_rus='слово 5 недель назад',
            updated_at=self.day_today - timedelta(weeks=5),
        )

        # Дата добавления первого слова (`<class 'datetime.datetime'>`).
        # Используется для задания начала периода фильтрации.
        self.begin_date_period = (
            WordModel.objects.order_by('updated_at').first().updated_at
        )

        # Url выбора параметров поиска для фильтрации слов.
        # `<class 'django.utils.functional.lazy.<locals>.__proxy__'>`
        self.start_words_study_url = reverse_lazy(
            'english:words_study', kwargs={'task_status': 'start'}
        )

    def test_period_only_today(self):
        """Тест фильтра слов по периоду "только сегодня".
        """
        querydict = {'start_period': '1', 'end_period': '1'}
        include_parameters, _ = create_lookup_parameters(querydict)
        filtered_words = WordModel.objects.filter(**include_parameters)

        self.assertTrue(filtered_words.contains(self.word_added_today))
        self.assertFalse(filtered_words.contains(self.word_added_3_days_ago))

    def test_period_3_days_ago_till_today(self):
        """Тест фильтра слов по периоду "3 дня назад" до "только сегодня".
        """
        querydict = {'start_period': '3', 'end_period': '1'}
        include_parameters, _ = create_lookup_parameters(querydict)
        filtered_words = WordModel.objects.filter(**include_parameters)

        self.assertTrue(filtered_words.contains(self.word_added_today))
        self.assertTrue(filtered_words.contains(self.word_added_3_days_ago))
        self.assertFalse(filtered_words.contains(self.word_added_3_week_ago))

    def test_period_4_week_ago_till_1_week_ago(self):
        """Тест фильтра слов по периоду "4 недели назад" до "неделя назад"."""
        querydict = {'start_period': '4', 'end_period': '3'}
        include_parameters, _ = create_lookup_parameters(querydict)
        filtered_words = WordModel.objects.filter(**include_parameters)

        self.assertTrue(filtered_words.contains(self.word_added_3_week_ago))
        self.assertFalse(filtered_words.contains(self.word_added_3_days_ago))
        self.assertFalse(filtered_words.contains(self.word_added_5_week_ago))

    def test_period_not_choised_till_1_week_ago(self):
        """Тест фильтра слов по периоду "не выбран" до "неделя назад"."""
        querydict = {'start_period': '9', 'end_period': '3'}
        include_parameters, _ = create_lookup_parameters(querydict)
        filtered_words = WordModel.objects.filter(**include_parameters)

        self.assertTrue(filtered_words.contains(self.word_added_3_week_ago))
        self.assertFalse(filtered_words.contains(self.word_added_3_days_ago))

    def test_period_not_choised_till_today(self):
        """Тест фильтра слов по периоду "не выбран" до "сегодня"."""
        querydict = {'start_period': '9', 'end_period': '1'}
        include_parameters, _ = create_lookup_parameters(querydict)
        filtered_words = WordModel.objects.filter(**include_parameters)

        self.assertTrue(filtered_words.contains(self.word_added_today)),
        self.assertTrue(filtered_words.contains(self.word_added_5_week_ago))


class TestAdaptLookupParameters(TestCase):
    """Тест получения из request параметров поиска слов для задачи.
    """

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        self.querydict = {
            'csrfmiddlewaretoken': ['SfNSD...hpwu7soCX'],
            'words_favorites': ['1'],
            'category_id': [''],
            'source_id': [''],
            'word_count': ['OW', 'CB'],
            'assessment': ['studying', 'examination']
        }

        self.begin_date_period = (
            WordModel.objects.order_by('updated_at').first().updated_at
        )
        # В word_count__in программно добавляется 'NC'.
        self.include_parameters = {
            'favorites__pk': 1,
            'word_count__in': ['OW', 'CB', 'NC'],
            'updated_at__range': (
                self.begin_date_period.strftime(
                    '%Y-%m-%d 00:00:00+00:00'),
                datetime.datetime.now(tz=timezone.utc).strftime(
                    '%Y-%m-%d 23:59:59+00:00'),
            ),
        }
        self.exclude_parameters = {
            'worduserknowledgerelation__knowledge_assessment__in': [7, 8, 11],
        }

        # Url выбора параметров поиска для фильтрации слов.
        self.start_words_study_url = reverse_lazy(
            'english:words_study', kwargs={'task_status': 'start'}
        )

    def test_add_to_lookup_parameters_new_words(self):
        """Тест включить в фильтр слова, еще не имеющие оценку уровня знания.

        Создан для устранения существующей ошибки, не попадали в задачу вновь
        добавленные слова и не имеющие оценку.
        """
        new_word = WordModel.objects.create(
            words_eng='new word', words_rus='новое слово',
        )
        include_parameters = {
            'word_count__in': ['OW', 'CB', 'NC'],
            'updated_at__range': (
                self.begin_date_period.strftime(
                    '%Y-%m-%d 00:00:00+00:00'),
                datetime.datetime.now(tz=timezone.utc).strftime(
                    '%Y-%m-%d 23:59:59+00:00'),
            ),
        }
        words = WordModel.objects.filter(
            **include_parameters
        ).exclude(
            **self.exclude_parameters
        )
        self.assertTrue(words.contains(new_word))

    def test_create_lookup_parameters(self):
        """Тест получения из request и переименования параметров поиска в БД.
        """
        include_parameters, exclude_parameters = create_lookup_parameters(
            self.querydict
        )
        self.assertEqual(self.include_parameters, include_parameters)
        self.assertEqual(self.exclude_parameters, exclude_parameters)

    def test_knowledge_assessment_by_users(self):
        """Тест фильтра слов по knowledge_assessment конкретного пользователя.

        Модель с отношениями m2m.
        Значение knowledge_assessment слов других пользователей не должно
        учитываться при фильтрации слов для текущего пользователя.
        """
        manager = WordModel.objects
        words = manager.filter(
            worduserknowledgerelation__knowledge_assessment__in=Subquery(
                WordUserKnowledgeRelation.objects.exclude(
                    knowledge_assessment__in=[7, 8, 9, 10, 11]
                ).values('knowledge_assessment')
            ),
            worduserknowledgerelation__user_id__exact=2,
        )

        self.assertTrue(words.contains(manager.get(id=1)))
        self.assertTrue(words.contains(manager.get(id=2)))
        self.assertTrue(words.contains(manager.get(id=6)))


class TestRandomFunctions(TestCase):
    """Тест функций, возвращающих случайные значения.

        Целями теста являются:
            - завершение выполнения функции без ошибки;
            - возвращение заданного количества объектов;
            - изменение последовательности объектов.
        """

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        self.queryset = WordModel.objects.all()
        self.number_words_in_question = 1

    def test_get_random_query_from_queryset(self):
        """Тест получи случайную модель из QuerySet."""
        random_query = get_random_query_from_queryset(self.queryset)

        translations = [random_query.words_eng, random_query.words_rus]
        question, answer = shuffle_sequence(translations)
        self.assertTrue(self.queryset.count() > self.number_words_in_question)
        self.assertTrue(isinstance(question, str))
