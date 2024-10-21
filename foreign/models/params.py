"""User task settings modul."""

from django.contrib.postgres.fields import ArrayField
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
)
from foreign.models import WordCategory, WordSource
from users.models import UserApp


class TranslateParams(models.Model):
    """Foreign words learning exercise user parameters.

    Including contains lookup parameters words for learning them.
    """

    user = models.OneToOneField(
        UserApp,
        on_delete=models.CASCADE,
    )
    """User that setting model stored (`UserApp`).
    """
    language_order = models.CharField(
        choices=LANGUAGE_ORDER_CHOICE,
        default=DEFAULT_LANGUAGE_ORDER,
        max_length=2,
        verbose_name='Порядок перевода',
    )
    """The order in which language translations of words are displayed.
    Could be:

    - first the question is in Foreign, then the answer is in
      Russian;
    - first the question is in Russian, then the answer is in
      Foreign;
    - random order.
    """
    timeout = models.PositiveSmallIntegerField(
        default=DEFAULT_TIMEOUT,
        verbose_name='Таймаут',
    )
    """Show the learning word time, sec (`int`).
    """
    favorites = models.BooleanField(
        default=False,
        verbose_name='Избранное',
    )
    """Wil be display only favorites words if `True`, all otherwise
    (`bool`).
    """
    category = models.ForeignKey(
        WordCategory,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Категория',
    )
    """If a category is selected, words from the specific category
    will be displayed.
    """
    source = models.ForeignKey(
        WordSource,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Источник',
    )
    """If a source is selected, words from the specific source will be
    displayed.
    """
    progress = models.CharField(
        choices=PROGRESS_CHOICES,
        default=DEFAULT_PROGRESS,
        max_length=1,
        verbose_name='Уровень знания',
    )
    """Current word learning progress level.
    """
    word_count = ArrayField(
        models.CharField(max_length=16),
        default=DEFAULT_WORD_COUNT,
        verbose_name='Длина выражения',
    )
    """Length of verbal expression.
    """
    period_start_date = models.CharField(
        choices=const.EDGE_PERIOD_CHOICES,
        default=NOT_CHOICES,
        max_length=2,
        verbose_name='Добавлено после',
    )
    """Start edge period for choice added words.
    """
    period_end_date = models.CharField(
        choices=const.EDGE_PERIOD_CHOICES,
        default=TODAY,
        max_length=2,
        verbose_name='Добавлено до',
    )
    """Start edge period for choice added words.
    """

    def __str__(self) -> str:
        """Represent an instance as a string."""
        return f'{self.user} настройки'

    class Meta:
        """Set model features."""

        verbose_name = 'Настройки "Изучаем слова"'
        verbose_name_plural = 'Настройки "Изучаем слова"'
