"""Defines discipline model."""

from django.core.validators import validate_slug
from django.db import models


class Discipline(models.Model):
    """Discipline model."""

    name = models.CharField(
        max_length=50,
        verbose_name='Дисциплина',
    )
    slug = models.SlugField(
        unique=True,
        validators=[validate_slug],
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'

    def __str__(self) -> str:
        """Get string representations of model instance."""
        return str(self.name)
