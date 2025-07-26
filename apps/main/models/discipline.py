"""Defines project discipline model."""

from django.db import models


# TODO: Develop
class Discipline(models.Model):
    """Project discipline model."""

    name = models.CharField(
        max_length=30,
    )

    class Meta:
        """Model configuration."""

        managed = False
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'
