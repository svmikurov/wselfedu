"""English language translation exercise."""

from django.db import models

from apps.core.models import AbstractBaseModel

__all__ = (
    'EnglishTranslationExercise',
    'EnglishTranslationStudyProgress',
)


class EnglishTranslationExercise(AbstractBaseModel):
    """English exercise translation.

    Exercise with specific translations.
    """

    exercise = models.ForeignKey(
        'lang.LanguageExercise',
        on_delete=models.CASCADE,
        verbose_name='Exercise',
        related_name='translations',
    )
    translation = models.ForeignKey(
        'lang.EnglishTranslation',
        on_delete=models.CASCADE,
        verbose_name='Translation',
        related_name='exercises',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Translation exercise'
        verbose_name_plural = 'Translation exercises'

        unique_together = ['exercise', 'translation']

        db_table = 'lang_english_exercise_translation_progress'


class EnglishTranslationStudyProgress(AbstractBaseModel):
    """English translation study progress for exercise."""

    user = models.ForeignKey(
        'users.Person',
        on_delete=models.CASCADE,
        verbose_name='Student',
    )
    exercise = models.ForeignKey(
        EnglishTranslationExercise,
        on_delete=models.CASCADE,
        verbose_name='English exercise translation relationship',
    )
    translation = models.ForeignKey(
        'lang.EnglishTranslation',
        on_delete=models.CASCADE,
        verbose_name='Translation',
    )
    value = models.PositiveSmallIntegerField(
        verbose_name='Progress value',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Translation study progress for exercise'
        verbose_name_plural = 'Translation study progress for exercise'

        unique_together = ['user', 'translation']

        db_table = 'lang_english_translation_exercise_progress'
