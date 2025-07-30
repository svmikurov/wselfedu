"""Defines abstract base exercise model."""

from django.db import models


class BaseExercise(models.Model):
    """Absract base exercise model.

    Postgres is created for inheritance.
    """

    name = models.CharField(
        max_length=30,
        verbose_name='Наименование',
    )
    created_at = models.DateTimeField(
        blank=True,
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        blank=True,
        auto_now=True,
    )

    class Meta:
        """Model configuration."""

        abstract = True
