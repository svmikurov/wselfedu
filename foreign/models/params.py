"""User task settings modul."""

from django.contrib.postgres.fields import ArrayField
from django.db import models

from config.constants import (
    DEFAULT_LANGUAGE_ORDER,
    DEFAULT_WORD_COUNT,
    LANGUAGE_ORDER_CHOICE,
    WORD_COUNT_CHOICE,
)
from contrib.models.params import ExerciseParams
from foreign.models import WordCategory, WordSource


class TranslateParams(ExerciseParams):
    """Foreign words learning exercise user parameters.

    Including contains lookup parameters words for learning them.
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
      Native;
    - first the question is in Russian, then the answer is in
      Native;
    - random order.
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
    word_count = ArrayField(
        models.CharField(
            max_length=16,
            choices=WORD_COUNT_CHOICE[1:],
        ),
        default=DEFAULT_WORD_COUNT,
        verbose_name='Длина выражения',
    )
    """Length of verbal expression.
    """

    def __str__(self) -> str:
        """Represent an instance as a string."""
        return f'{self.user} настройки'

    class Meta:
        """Set model features."""

        verbose_name = 'Настройки "Изучаем слова"'
        verbose_name_plural = 'Настройки "Изучаем слова"'
