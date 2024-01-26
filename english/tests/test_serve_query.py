"""Тест модуля test_serve_query.py
"""

from django.test import TestCase

from english.models import WordModel
from english.services.serve_query import (
    all_objects,
    filter_objects,
    get_objects,
)


class TestServeQuery(TestCase):
    """Тест модуля test_serve_query.py"""

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        self.manager = WordModel.objects
        self.kwargs = {'word_count': 'OW', 'id': 6}

    def test_get_objects(self):
        """Тест получения объекта от менеджера модели.
        """
        expected_words = self.manager.get(**self.kwargs)
        received_words = get_objects(self.manager, **self.kwargs)
        self.assertEqual(expected_words, received_words)

    def test_all_objects(self):
        """Тест получения всех объектов от менеджера модели.
        """
        expected_words = self.manager.all()
        received_words = all_objects(self.manager)
        self.assertEqual(list(expected_words), list(received_words))

    def test_filter_objects(self):
        """Тест применения фильтра к менеджеру модели.
        """
        expected_words = self.manager.filter(**self.kwargs)
        received_words = filter_objects(self.manager, **self.kwargs)
        self.assertEqual(list(expected_words), list(received_words))
