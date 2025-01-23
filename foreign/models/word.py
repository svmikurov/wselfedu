"""Foreign words translate dictionary."""

from django.db import models

from foreign.models.category import WordCategory
from foreign.models.source import WordSource
from users.models import UserApp


class Word(models.Model):
    """Foreign words."""

    user = models.ForeignKey(
        UserApp,
        on_delete=models.CASCADE,
        related_name='user_word',
        verbose_name='Пользователь, который добавил слово',
    )
    foreign_word = models.CharField(
        max_length=75,
        verbose_name='Слово на иностранном',
        help_text='Не более 75 символов.',
    )
    native_word = models.CharField(
        max_length=75,
        verbose_name='Слово на родном',
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
    progress = models.ManyToManyField(
        UserApp,
        through='WordProgress',
        blank=True,
        related_name='word_knowledge',
        verbose_name='Прогресс изучения слова',
    )
    favorites = models.ManyToManyField(
        UserApp,
        through='WordFavorites',
        blank=True,
        related_name='word_favorites',
        verbose_name='Является ли слово избранным',
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
        """Model features."""

        verbose_name = 'Словарь иностранных слов'
        verbose_name_plural = 'Словарь иностранных слов'
        ordering = ['pk']

    def __str__(self) -> str:
        """Provide the informal string representation of an object."""
        return self.foreign_word


class WordProgress(models.Model):
    """User's progress of word study."""

    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    user = models.ForeignKey(UserApp, on_delete=models.CASCADE)
    progress = models.DecimalField(max_digits=2, decimal_places=0, default=0)

    class Meta:
        """Model features."""

        unique_together = [['word', 'user']]
        verbose_name = 'Оценка пользователем знания слова'
        verbose_name_plural = 'Оценки пользователем знания слова'

    def __str__(self) -> str:
        """Provide the informal string representation of an object."""
        return str(self.progress)


class WordFavorites(models.Model):
    """Model for store users favorites words."""

    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    user = models.ForeignKey(UserApp, on_delete=models.CASCADE)

    class Meta:
        """Model features."""

        unique_together = [['word', 'user']]
        verbose_name = 'Избранное слово'
        verbose_name_plural = 'Избранные слова'

    def __str__(self) -> str:
        """Provide the informal string representation of an object."""
        return f'Слово {self.word} избрано {self.user}'


class AssignedWord(models.Model):
    """Words assigned to a student by a mentor."""

    word = models.ManyToManyField(
        Word,
        blank=True,
        related_name='assigned_word',
        verbose_name='Назначенное слово',
    )
    student = models.ForeignKey(
        UserApp,
        on_delete=models.CASCADE,
        related_name='assigned_student',
        verbose_name='Назначено слово студенту',
    )

    class Meta:
        """Model features."""

        verbose_name = 'Назначенное слово для изучения'
        verbose_name_plural = 'Назначенные слова для изучения'
