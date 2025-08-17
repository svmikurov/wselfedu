"""Defines project exercise collection model."""

from typing import Any

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.core.models import Discipline
from apps.core.models.base import BaseExercise


class TaskIO(models.Model):
    """String representation model of the I/O task type."""

    name = models.CharField(
        'Тип ввода/вывода',
        max_length=50,
    )
    alias = models.SlugField(
        'Псевдоним',
        max_length=50,
        unique=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        """Configure the model."""

        verbose_name = 'Тип I/O'
        verbose_name_plural = 'Тип I/O'
        db_table = 'core_task_io'

    def __str__(self) -> str:
        """Get the string representation of model instance."""
        return str(self.name)


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
    task_io = models.ForeignKey(
        TaskIO,
        on_delete=models.CASCADE,
        help_text='Task I/O: text, number, test, ...',
        verbose_name='Тип ввода/вывода',
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
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        'Изменено',
        auto_now=True,
    )

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
