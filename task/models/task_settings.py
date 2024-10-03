"""User task settings modul."""

from django.db import models

from config import constants as const
from config.constants import (
    DEFAULT_LANGUAGE_ORDER,
    DEFAULT_PROGRESS,
    DEFAULT_TIMEOUT,
    DEFAULT_WORD_COUNT,
    LANGUAGE_ORDER_CHOICE,
    NOT_CHOICES,
    PROGRESS_CHOICES,
    TODAY,
    WORD_COUNT_CHOICE,
)
from english.models import CategoryModel, SourceModel
from users.models import UserModel


class ForeignExerciseSettings(models.Model):
    """Foreign words learning exercise user settings model.

    Including contains lookup parameters words for learning them.

    Attributes
    ----------
    user : `UserModel`
        User that setting model stored.
    language_order : `str`
        The order in which language translations of words are displayed.

        Could be:
            - first the question is in Foreign, then the answer is in
              Russian;
            - first the question is in Russian, then the answer is in
              Foreign;
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

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
    )
    language_order = models.CharField(
        choices=LANGUAGE_ORDER_CHOICE,
        default=DEFAULT_LANGUAGE_ORDER,
        max_length=2,
        verbose_name='Порядок перевода',
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
        choices=PROGRESS_CHOICES,
        default=DEFAULT_PROGRESS,
        max_length=1,
        verbose_name='Уровень знания',
    )
    word_count = models.CharField(
        choices=WORD_COUNT_CHOICE,
        default=DEFAULT_WORD_COUNT,
        max_length=2,
        verbose_name='Длина выражения',
    )
    date_start = models.CharField(
        choices=const.EDGE_PERIOD_CHOICES,
        default=NOT_CHOICES,
        max_length=2,
        verbose_name='Добавлено после',
    )
    date_end = models.CharField(
        choices=const.EDGE_PERIOD_CHOICES,
        default=TODAY,
        max_length=2,
        verbose_name='Добавлено до',
    )

    def __str__(self) -> str:
        """Represent an instance as a string."""
        return f'{self.user} настройки'

    class Meta:
        """Set model features."""

        verbose_name = 'Настройки "Изучаем слова"'
        verbose_name_plural = 'Настройки "Изучаем слова"'
