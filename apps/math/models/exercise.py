"""Defines math app exercise type model."""

from django.db import models


# TODO: Check consistency with SQL-script
class MathExercise(models.Model):
    """Math app exercise type model."""

    name = models.CharField(
        max_length=30,
        verbose_name='Наименование',
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
        db_table = 'math"."exercise'
        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'
