"""Defines math app exercise type model."""

from django.db import models


class MathExercise(models.Model):
    """Math app exercise type model."""

    name = models.CharField(
        max_length=30,
        verbose_name='Упражнение',
    )
    created_at = models.DateTimeField(
        blank=True,
    )
    updated_at = models.DateTimeField(
        blank=True,
    )

    class Meta:
        """Model configuration."""

        managed = False
        db_table = 'math_exercise'
        verbose_name = 'Математические упражнения'
        verbose_name_plural = 'Математические упражнения'
