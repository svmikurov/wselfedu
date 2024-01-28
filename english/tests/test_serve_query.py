"""Тест модуля test_serve_query.py
"""

from django.test import TestCase

from english.models import WordModel
from english.services.serve_query import (
    all_objects,
    filter_objects,
    get_objects,
    adapt_values_for_orm,
)
from users.models import UserModel


class TestServeQuery(TestCase):
    """Тест модуля test_serve_query.py"""

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        self.manager = WordModel.objects
        self.kwargs = {'word_count': 'OW', 'id': 6}

        user_id = UserModel.objects.get(username='user1').pk
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

    def test_get_objects(self):
        """Тест получения объекта от менеджера модели."""
        expected_words = self.manager.get(**self.kwargs)
        received_words = get_objects(self.manager, **self.kwargs)
        self.assertEqual(expected_words, received_words)

    def test_all_objects(self):
        """Тест получения всех объектов от менеджера модели."""
        expected_words = self.manager.all()
        received_words = all_objects(self.manager)
        self.assertEqual(list(expected_words), list(received_words))

    def test_filter_objects(self):
        """Тест фильтра по параметрам поиска."""
        words = filter_objects(WordModel.objects, **self.lookup_parameters)
        received_words_eng = words.values_list('words_eng', flat=True)
        self.assertEqual(set(received_words_eng), self.lookup_result)


class TestAdaptLookupParameters(TestCase):
    def setUp(self):
        self.frontend_lookup_parameters = {
            'words_favorites': 'user_id',
            'category_id': 'category_id',
            'source_id': 'source_id',
            'word_count': 'count',
            'assessment': 'level',
            'user_id': 'user_id',
        }

        self.model_lookup_parameters = {
            'favorites__pk': 'user_id',
            'category_id': 'category_id',
            'source_id': 'source_id',
            'word_count__in': 'count',
            'worduserknowledgerelation__knowledge_assessment__in': 'level',
            'worduserknowledgerelation__user_id': 'user_id',
        }

        self.lookup_parameters_keys = {
            'words_favorites': 'favorites__pk',
            'category_id': 'category_id',
            'source_id': 'source_id',
            'word_count': 'word_count__in',
            'assessment': 'worduserknowledgerelation__knowledge_assessment__in',
            'user_id': 'worduserknowledgerelation__user_id',
        }

    def test_adapt_values_for_orm(self):
        """Тест адаптации для ORM параметров поиска из frontend."""
        lookup_parameters = adapt_values_for_orm(
            self.frontend_lookup_parameters, self.lookup_parameters_keys
        )
        self.assertEqual(lookup_parameters, self.model_lookup_parameters)
