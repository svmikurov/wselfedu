"""Defines math app task model."""

from django.db import models

MAX_OPERAND_DIGIT = 3
DECIMAL_PACES = 3


# TODO: Develop
class CalculationTask(models.Model):
    """Calculation math task model."""

    exercise = models.ForeignKey(
        'MathExercise',
        on_delete=models.CASCADE,
        related_name='calc_tasks',
        editable=False,
    )
    operand_1 = models.DecimalField(
        max_digits=MAX_OPERAND_DIGIT,
        decimal_places=DECIMAL_PACES,
        editable=False,
    )
    operand_2 = models.DecimalField(
        max_digits=MAX_OPERAND_DIGIT,
        decimal_places=DECIMAL_PACES,
        editable=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        """Model configuration."""

        managed = False
        db_table = 'math"."calculation_task'
