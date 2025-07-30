"""Defines math app exercise type model."""

from apps.core.models import BaseExercise


class MathExercise(BaseExercise):
    """Math app exercise type model."""

    class Meta:
        """Model configuration."""

        managed = False
        db_table = 'math"."exercise'
        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'
