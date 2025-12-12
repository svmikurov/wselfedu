"""Word model."""

from django.contrib.auth import get_user_model
from django.db import models


class AbstractWordModel(models.Model):
    """Base word model."""

    WORD_LENGTH = 70

    word: models.CharField  # type: ignore[type-arg]

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Изменено',
    )

    class Meta:
        """Model configuration."""

        abstract = True

    def __str__(self) -> str:
        """Get string representation."""
        return str(self.word)


class NativeWord(AbstractWordModel):
    """Native word."""

    user = models.ForeignKey(
        get_user_model(),
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
        get_user_model(),
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
        db_table = 'lang_word_english'
