"""Defines discipline model."""

from django.db import models


class Discipline(models.Model):
    """Discipline model."""

    name = models.CharField(
        max_length=30,
        verbose_name='Наименование дисциплины',
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления',
    )

    class Meta:
        """Configure the model."""

        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'
