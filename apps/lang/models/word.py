"""Word models."""

from django.db import models

from .abstract.word import AbstractWordModel

__all__ = [
    'NativeWord',
    'EnglishWord',
]


class NativeWord(AbstractWordModel):
    """Native word."""

    user = models.ForeignKey(
        'users.Person',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='native_word',
    )
    word = models.CharField(
        max_length=AbstractWordModel.WORD_LENGTH,
        verbose_name='Слово на родном языке',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Слово родного языка'
        verbose_name_plural = 'Слова родного языка'

        unique_together = ['user', 'word']

        db_table = 'lang_word_native'


class EnglishWord(AbstractWordModel):
    """English word."""

    user = models.ForeignKey(
        'users.Person',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='english_word',
    )
    word = models.CharField(
        max_length=AbstractWordModel.WORD_LENGTH,
        verbose_name='Слово на английском',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Английское слово'
        verbose_name_plural = 'Английские слова'

        unique_together = ['user', 'word']

        db_table = 'lang_english_word'
