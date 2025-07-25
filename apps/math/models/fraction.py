"""Defines math fraction task model."""

from django.db import models

from apps.main.models import BaseTask


class FractionTask(BaseTask):
    """Math fraction task model."""

    exercise = models.ForeignKey(
        'MathExercise',
        on_delete=models.CASCADE,
    )

    class Meta:
        """Model configuration."""

        db_table = 'math"."fraction_task'
