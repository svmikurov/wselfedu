"""Translation exercise models."""

from django.db import models

from apps.core.models import AbstractBaseModel

__all__ = [
    'EnglishTranslationExercise',
    'EnglishTranslationProgress',
]


class EnglishTranslationExercise(AbstractBaseModel):
    """English exercise translation."""

    exercise = models.ForeignKey(
        'lang.Exercise',
        on_delete=models.CASCADE,
        verbose_name='Упражнение',
    )
    translation = models.ForeignKey(
        'lang.EnglishTranslation',
        on_delete=models.CASCADE,
        verbose_name='Перевод',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Перевод упражнения'
        verbose_name_plural = 'Переводы упражнения'

        unique_together = ['exercise', 'translation']

        db_table = 'lang_english_exercise_translation'


class EnglishTranslationProgress(AbstractBaseModel):
    """User progress in learning English translation."""

    user = models.ForeignKey(
        'users.Person',
        on_delete=models.CASCADE,
        verbose_name='Студент',
    )
    translation = models.ForeignKey(
        'lang.EnglishTranslation',
        on_delete=models.CASCADE,
        verbose_name='Перевод',
    )
    value = models.PositiveSmallIntegerField(
        verbose_name='Значение',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Прогресс изучения перевода'
        verbose_name_plural = 'Прогресс изучения переводов'

        unique_together = ['user', 'translation']

        db_table = 'lang_english_translation_progress'
