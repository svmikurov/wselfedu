"""Defines project exercise collection model."""

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import validate_slug
from django.db import models

from apps.core.models import Discipline


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
    slug = models.SlugField(
        validators=[validate_slug],
        unique=True,
    )
    task_io = models.ForeignKey(
        'TaskIO',
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

    def __str__(self) -> str:
        """Get the string representation of model instance."""
        return str(self.name)
