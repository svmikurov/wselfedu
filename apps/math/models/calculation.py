"""Defines math app task model."""

from django.db import models

from apps.main.models import BaseTask


class CalculationTask(BaseTask):
    """Calculation math task model."""

    exercise = models.ForeignKey(
        'MathExercise',
        on_delete=models.CASCADE,
        related_name='calc_tasks',
        editable=False,
    )
    operand_1 = models.DecimalField(
        max_digits=3,
        decimal_places=0,
        editable=False,
    )
    operand_2 = models.DecimalField(
        max_digits=3,
        decimal_places=0,
        editable=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        """Model configuration."""

        db_table = 'math"."calculation_task'
