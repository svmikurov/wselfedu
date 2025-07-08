"""Defines task models."""

from django.db import models

from apps.users.models import CustomUser
from base.models.uid import UIDModel


class MathTaskChoice(models.Choices):
    """Mathematical task choices."""

    ADDING = 'adding'
    SUBTRACTION = 'subtraction'
    MULTIPLICATION = 'multiplication'
    DIVISION = 'division'


class SimpleTask(UIDModel):
    """Simple calculation task madel."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    exercise_name = models.CharField(
        max_length=30,
        choices=MathTaskChoice,
    )
    operand_1 = models.SmallIntegerField()
    operand_2 = models.SmallIntegerField()
    created_at = models.DateTimeField()
    user_answer = models.SmallIntegerField()
    is_correct = models.BooleanField()
    checked_at = models.DateTimeField()

    class Meta:
        """Configure the model."""

        db_table = 'math_simple_task'
