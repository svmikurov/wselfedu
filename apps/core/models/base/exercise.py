"""Defines abstract base exercise model."""

from django.db import models

from apps.core.models import Discipline


class BaseExercise(models.Model):
    """Absract base exercise model."""

    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.CASCADE,
        verbose_name='Дисциплина',
        help_text='Exercise in discipline',
    )
    name = models.CharField(
        max_length=50,
        verbose_name='Наименование',
        unique=True,
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

    def __str__(self) -> str:
        """Get the string representation of model instance."""
        return str(self.name)
