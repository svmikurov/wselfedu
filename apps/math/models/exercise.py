"""Defines math app exercise type model."""

from apps.core.models.base import BaseExercise


class MathExercise(BaseExercise):
    """Math app exercise type model."""

    class Meta:
        """Model configuration."""

        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'
