"""Defines abstract base exercise model."""

from django.db import models


class BaseExercise(models.Model):
    """Absract base exercise model."""

    name = models.CharField(
        max_length=50,
        verbose_name='Наименование',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        """Model configuration."""

        abstract = True
