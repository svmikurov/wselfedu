"""Word translation models."""

from django.contrib.auth import get_user_model
from django.db import models

from apps.core.models import Source


class EnglishTranslation(models.Model):
    """Translation of English word."""

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    native = models.ForeignKey(
        'NativeWord',
        on_delete=models.CASCADE,
        verbose_name='Слово на родном языке',
    )
    english = models.ForeignKey(
        'EnglishWord',
        on_delete=models.CASCADE,
        verbose_name='Слово на английском',
    )
    category = models.ForeignKey(
        'LangCategory',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Категория',
    )
    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Источник',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлен',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Изменен',
    )

    class Meta:
        """Configure the model."""

        verbose_name = 'Перевод слова на английский'
        verbose_name_plural = 'Переводы слов на английский'
        db_table = 'lang_translation_english'

    def __str__(self) -> str:
        """Get the string representation of model instance."""
        return str(f'{self.native} - {self.english}')
