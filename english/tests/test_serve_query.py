"""Тест модуля test_serve_query.py
"""

from django.test import TestCase

from english.models import WordModel
from english.services.serve_query import (
    get_random_query_from_queryset,
    get_lookup_parameters,
)
from english.tasks.study_words import shuffle_sequence


class TestAdaptLookupParameters(TestCase):
    def setUp(self):
        self.querydict = {
            'csrfmiddlewaretoken': ['SfNSD...hpwu7soCX'],
            'words_favorites': ['1'],
            'category_id': [''],
            'source_id': [''],
            'word_count': ['OW', 'CB'],
            'assessment': ['studying', 'examination']
        }
        self.expected_lookup_parameters = {
            'favorites__pk': 1,
            'word_count__in': ['OW', 'CB'],
            'worduserknowledgerelation__knowledge_assessment__in': [
                0, 1, 2, 3, 4, 5, 6, 9, 10
            ]
        }

    def test_get_lookup_parameters(self):
        """Тест получения из request и переименования параметров поиска в БД.
        """
        lookup_parameters = get_lookup_parameters(self.querydict)
        self.assertEqual(self.expected_lookup_parameters, lookup_parameters)


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
