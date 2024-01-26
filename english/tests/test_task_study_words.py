"""Модуль тестирования упражнения Изучение слов.

"""

from django.test import TestCase


class TestChooseEnglishWordsStudy(TestCase):
    """Протестируй выбор пользователем слов для изучения.
    """

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        self.user = ...
