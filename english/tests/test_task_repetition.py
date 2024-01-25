# TODO

"""Тест чекбокса "Выбери уровень знания слов" в упражнении "Изучаем слова".
"""

from django.test import TestCase

from english.models import WordModel
# from english.tasks.repetition_task import filter_repetition_words


class TestFilterWordsRepetitionTask(TestCase):
    """Тест чекбокса "Выбери уровень знания слов" в упражнении "Изучаем слова".
    """

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        self.user = WordModel.objects.get(pk=2)
        obj = WordModel.objects
        # QuerySet отфильтрованных слов по "изучаю".
        self.filter_learn_words = obj.filter(pk=2)
        # QuerySet отфильтрованных слов по "повторяю".
        self.filter_repeat_words = obj.filter(pk=3)
        # QuerySet отфильтрованных слов по "проверяю".
        self.filter_test_words = obj.filter(pk=4)
        # QuerySet отфильтрованных слов по "знаю".
        self.filter_learned_words = obj.filter(pk=5)
