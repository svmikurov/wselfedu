"""Translation exercise."""

from django.db import models


class EnglishExerciseTranslation(models.Model):
    """English exercise translation."""

    exercise = models.ForeignKey(
        'LangExercise',
        on_delete=models.CASCADE,
        verbose_name='Упражнение',
    )
    translation = models.ForeignKey(
        'EnglishTranslation',
        on_delete=models.CASCADE,
        verbose_name='Перевод',
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
        """Model configuration."""

        verbose_name = 'Перевод упражнения'
        verbose_name_plural = 'Переводы упражнения'

        unique_together = ['exercise', 'translation']

        db_table = 'lang_english_exercise_translation'


class EnglishTranslationProgress(models.Model):
    """User progress in learning English translation."""

    user = models.ForeignKey(
        'users.Person',
        on_delete=models.CASCADE,
        verbose_name='Студент',
    )
    translation = models.ForeignKey(
        'EnglishTranslation', on_delete=models.CASCADE, verbose_name='Перевод'
    )
    value = models.PositiveSmallIntegerField(verbose_name='Значение')

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

        verbose_name = 'Прогресс изучения перевода'
        verbose_name_plural = 'Прогресс изучения переводов'

        unique_together = ['user', 'translation']

        db_table = 'lang_english_translation_progress'
