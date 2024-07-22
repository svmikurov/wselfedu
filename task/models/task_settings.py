"""
User task settings modul.
"""

from django.db import models

from english.models import CategoryModel, SourceModel
from task.forms.english_translate_choice_form import EDGE_PERIODS_ALIASES
from users.models import UserModel


class EnglishTaskSettings(models.Model):
    """English learning task user settings model.

    Including contains lookup parameters words for learning them.

    Attributes
    ----------
    user : `UserModel`
        User that setting model stored.
    language_order : `str`
        The order in which language translations of words are displayed.

        Could be:
            - first the question is in English, then the answer is in
              Russian;
            - first the question is in Russian, then the answer is in
              English;
            - random order.

    timeout : `int`
        Show the learning word time, sec.
    favorites : `bool`
        Wil be display only favorites words if `True`, all otherwise.
    category : `CategoryModel`
        If a category is selected, words from the specific category
        will be displayed.
    source : `SourceModel`
        If a source is selected, words from the specific source will be
        displayed.
    knowledge : `str`
        Current knowledge word level.
    word_count : `str`
        Length of verbal expression.
    date_start : `str`
        Start edge period for choice added words.
    date_end : `str`
        Start edge period for choice added words.
    """

    LANGUAGE_ORDER = [
        ('RN', 'Перевод в случайном порядке'),
        ('EN', 'Перевод с английского языка'),
        ('RU', 'Перевод на английский язык'),
    ]
    DEFAULT_START_PERIOD = ('NC', 'Добавлено')
    DEFAULT_END_PERIOD = ('DT', 'Сегодня')
    WORD_COUNT = (
        ('OW', 'Слово'),
        ('CB', 'Словосочетание'),
        ('PS', 'Часть предложения'),
        ('ST', 'Предложение'),
    )
    KNOWLEDGE_ASSESSMENT = (
        ('S', 'Изучаю'),  # study
        ('R', 'Повторяю'),  # repeat
        ('E', 'Проверяю'),  # examination
        ('K', 'Знаю'),  # know
    )
    DEFAULT_LANGUAGE_ORDER = LANGUAGE_ORDER[0]
    DEFAULT_KNOWLEDGE_ASSESSMENT = 'S'
    DEFAULT_WORD_COUNT = ('OW', 'CB')
    DEFAULT_CREATE_CHOICE_VALUE = 0
    DEFAULT_TIMEOUT = 5

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
    )
    language_order = models.CharField(
        choices=LANGUAGE_ORDER,
        default=DEFAULT_LANGUAGE_ORDER,
        max_length=2,
        verbose_name='Порядок перевода'
    )
    timeout = models.PositiveSmallIntegerField(
        default=DEFAULT_TIMEOUT,
        verbose_name='Таймаут',
    )
    favorites = models.BooleanField(
        default=False,
        verbose_name='Избранное',
    )
    category = models.ForeignKey(
        CategoryModel,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Категория',
    )
    source = models.ForeignKey(
        SourceModel,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Источник',
    )
    knowledge = models.CharField(
        choices=KNOWLEDGE_ASSESSMENT,
        default=DEFAULT_KNOWLEDGE_ASSESSMENT,
        max_length=1,
        verbose_name='Уровень знания',
    )
    word_count = models.CharField(
        choices=WORD_COUNT,
        default=DEFAULT_WORD_COUNT,
        max_length=2,
        verbose_name='Длина выражения',
    )
    date_start = models.CharField(
        choices=EDGE_PERIODS_ALIASES,
        default=DEFAULT_START_PERIOD,
        max_length=2,
        verbose_name='Добавлено после',
    )
    date_end = models.CharField(
        choices=EDGE_PERIODS_ALIASES[:-1],
        default=DEFAULT_END_PERIOD,
        max_length=2,
        verbose_name='Добавлено до',
    )

    def __str__(self):
        """Represent an instance as a string."""
        return f'{self.user} настройки'

    class Meta:
        verbose_name = 'Настройки "Изучаем слова"'
        verbose_name_plural = 'Настройки "Изучаем слова"'
