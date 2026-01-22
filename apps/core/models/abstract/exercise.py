"""Abstract base exercise model."""

from django.db import models
from django.utils.translation import gettext as _

from .base import AbstractBaseModel


class BaseExercise(AbstractBaseModel):
    """Abstract base exercise model."""

    discipline = models.ForeignKey(
        'core.Discipline',
        on_delete=models.CASCADE,
        verbose_name=_('Discipline'),
    )
    name = models.CharField(
        max_length=50,
        verbose_name=_('Exercise'),
        unique=True,
    )

    class Meta:
        """Model configuration."""

        abstract = True

    def __str__(self) -> str:
        """Get string representation."""
        return self.name
