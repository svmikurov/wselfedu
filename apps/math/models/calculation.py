"""Defines math app task model."""

from django.db import models

from apps.main.models import BaseTask


class CalculationTask(BaseTask):
    """Calculation math task model."""

    exercise = models.ForeignKey(
        'MathExercise',
        on_delete=models.CASCADE,
    )

    class Meta:
        """Model configuration."""

        db_table = 'math_calculation_task'
