"""Defines project exercise collection model."""

from typing import Any

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.core.models import Discipline
from apps.core.models.base import BaseExercise


def get_exercises_choices() -> dict[str, Any]:
    """Get exercise models for choice.

    Return model filter by base exercise model.
    """
    return {
        'model__in': [
            model._meta.model_name for model in BaseExercise.__subclasses__()
        ]
    }


class Exercise(models.Model):
    """Exercise registration from all disciplines."""

    name = models.CharField(
        max_length=100,
        help_text='Exercise name',
        verbose_name='Наименование упражнение',
    )
    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.CASCADE,
        help_text='Discipline',
        verbose_name='Дисциплина',
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        help_text='Exercise model in ContentType',
    )
    object_id = models.PositiveBigIntegerField(
        help_text='Primary key exercise name field in exercise model',
    )
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        """Configure the model."""

        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self) -> str:
        """Get the string representation of model instance."""
        return str(self.name)
