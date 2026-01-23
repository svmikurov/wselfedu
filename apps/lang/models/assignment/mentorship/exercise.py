"""Assigned exercise model."""

from django.db import models

from apps.core.models import AbstractBaseModel

__all__ = [
    'EnglishAssignedExercise',
]


class EnglishAssignedExercise(AbstractBaseModel):
    """Assigned English exercise."""

    mentorship = models.ForeignKey(
        'users.Mentorship',
        on_delete=models.CASCADE,
        verbose_name='Наставничество',
    )
    exercise = models.ForeignKey(
        'lang.Exercise',
        on_delete=models.CASCADE,
        verbose_name='Упражнение',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Назначенное упражнение по английскому'
        verbose_name_plural = 'Назначенные упражнения по английскому'

        db_table = 'lang_assigned_english_exercise'
