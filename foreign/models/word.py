"""Foreign words translate dictionary."""

from django.db import models

from config.constants import NOT_CHOICES, PK, USER, WORD, WORD_COUNT_CHOICE
from foreign.models.category import WordCategory
from foreign.models.source import WordSource
from users.models import UserApp


class Word(models.Model):
    """Foreign word translate dictionary."""

    user = models.ForeignKey(
        UserApp,
        on_delete=models.CASCADE,
        related_name='user_word',
        verbose_name='Пользователь, который изучает слово',
    )
    """User who studies the word.
    """
    mentor = models.ForeignKey(
        UserApp,
        on_delete=models.SET_NULL,
        null=True,
        related_name='mentor_word',
        verbose_name='Наставник, который добавил слово.',
    )
    """User who added the word.
    """
    foreign_word = models.CharField(
        max_length=75,
        verbose_name='Иностранное слово',
        help_text='Не более 75 символов.',
    )
    russian_word = models.CharField(
        max_length=75,
        verbose_name='Слово на русском',
        help_text='Не более 75 символов.',
    )
    source = models.ForeignKey(
        WordSource,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='get_source',
        verbose_name='Источник',
    )
    category = models.ForeignKey(
        WordCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория',
    )
    # https://docs.djangoproject.com/en/4.2/ref/models/fields/#choices
    word_count = models.CharField(
        max_length=2,
        choices=WORD_COUNT_CHOICE,
        default=NOT_CHOICES,
        verbose_name='Количество слов',
    )
    # A field that displays how the user rates his knowledge of this
    # word
    progress = models.ManyToManyField(
        UserApp,
        through='WordProgress',
        blank=True,
        related_name='word_knowledge',
    )
    # Does it word favorites for show?
    favorites = models.ManyToManyField(
        UserApp,
        through='WordFavorites',
        blank=True,
        related_name='word_favorites',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Изменено',
    )

    class Meta:
        """Set model features."""

        verbose_name = 'Словарь иностранных слов'
        verbose_name_plural = 'Словарь иностранных слов'
        ordering = [PK]

    def __str__(self) -> str:
        """Provide the informal string representation of an object."""
        return self.foreign_word


class WordProgress(models.Model):
    """User's assessment of word knowledge."""

    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    user = models.ForeignKey(UserApp, on_delete=models.CASCADE)
    progress = models.DecimalField(max_digits=2, decimal_places=0, default=0)

    class Meta:
        """Set model features."""

        unique_together = [[WORD, USER]]
        verbose_name = 'Оценка пользователем знания слова'
        verbose_name_plural = 'Оценки пользователем знания слова'

    def __str__(self) -> str:
        """Provide the informal string representation of an object."""
        return self.progress


class WordFavorites(models.Model):
    """Model for store users favorites words."""

    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    user = models.ForeignKey(UserApp, on_delete=models.CASCADE)

    class Meta:
        """Set model features."""

        unique_together = [[WORD, USER]]
        verbose_name = 'Избранное слово'
        verbose_name_plural = 'Избранные слова'

    def __str__(self) -> str:
        """Provide the informal string representation of an object."""
        return f'Слово {self.word} избрано {self.user}'
