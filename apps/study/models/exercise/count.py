"""Assigned exercise's task count."""

from django.db import models

from apps.core.models.abstract import AbstractBaseModel


class ExerciseTaskCount(AbstractBaseModel):
    """Exercise task count."""

    exercise = models.ForeignKey(
        'ExerciseAssigned',
        on_delete=models.CASCADE,
        verbose_name='Assigned exercise',
        related_name='exercise_task_count',
    )
    count = models.PositiveSmallIntegerField(
        verbose_name="Assigned exercise's task count",
    )

    class Meta:
        """Model configuration."""

        verbose_name = "Assigned exercise's task count"
        verbose_name_plural = "Assigned exercise's task count"
        db_table = 'study_assigned_task_count'
