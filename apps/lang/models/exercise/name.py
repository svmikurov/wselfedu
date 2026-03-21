"""Language discipline exercise."""

from django.db import models

from apps.core.models.abstract import BaseExercise

__all__ = ('LanguageExercise',)


class LanguageExercise(BaseExercise):
    """Language discipline exercise."""

    user = models.ForeignKey(
        'users.Person',
        on_delete=models.CASCADE,
        verbose_name='Exercise created by',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Exercise'
        verbose_name_plural = 'Exercises'

        unique_together = ['name', 'user']
