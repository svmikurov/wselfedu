"""Language discipline word translation model."""

from django.db import models

from apps.core.models import AbstractBaseModel

from .abstract import AbstractProgressModel

__all__ = [
    'EnglishTranslation',
]


class EnglishTranslation(
    AbstractProgressModel,
    AbstractBaseModel,
):
    """English translation of the word."""

    user = models.ForeignKey(
        'users.Person',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )

    native = models.ForeignKey(
        'NativeWord',
        on_delete=models.CASCADE,
        verbose_name='Слово на родном языке',
    )
    foreign = models.ForeignKey(
        'EnglishWord',
        on_delete=models.CASCADE,
        verbose_name='Слово на английском',
    )

    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Категория',
    )
    source = models.ForeignKey(
        'core.Source',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Источник',
    )
    marks = models.ManyToManyField(  # type: ignore[var-annotated]
        'Mark',
        through='TranslationMark',
        through_fields=('translation', 'mark'),
        blank=True,
        verbose_name='Маркеры',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Перевод слова на английский'
        verbose_name_plural = 'Переводы слов на английский'

        ordering = ['-created_at']

        db_table = 'lang_english_translation'
