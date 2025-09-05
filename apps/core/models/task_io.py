"""Defines string representation model of the I/O task type madel."""

from django.db import models


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
