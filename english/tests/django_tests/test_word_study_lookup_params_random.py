from django.test import TestCase

from english.models import WordModel
from english.services import get_random_query_from_queryset
from english.tasks.study_words import shuffle_sequence


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
