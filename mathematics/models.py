"""Mathematical exercises model module."""

from django.db import models

from config.constants import CALCULATION_TYPES
from users.models import UserApp


class MathematicsAnalytic(models.Model):
    """Mathematical exercises model.

    Stores tasks and user solutions for all mathematical exercises.
    The exercise contains two operands.
    The model stores only mathematical calculation
    :ref:`Mathematics exercise <reference/mathematics/exercise:Mathematics exercise>`.
    """  # noqa: E501, W505

    user = models.ForeignKey(UserApp, on_delete=models.CASCADE)
    """User performing the exercise.
    """
    calculation_type = models.CharField(
        choices=CALCULATION_TYPES,
        max_length=10,
    )
    """Type of mathematical calculation.
    """
    first_operand = models.SmallIntegerField()
    """First operand of the expression.
    """
    second_operand = models.SmallIntegerField()
    """Second operand of the expression.
    """
    user_solution = models.SmallIntegerField()
    """User task solution.
    """
    is_correctly = models.BooleanField(blank=True, null=True)
    """Marking the user's solution to the task as correct.
    """
    solution_time = models.PositiveSmallIntegerField()
    """Time spent by the user to solve the task.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    """Date and time of task creation.
    """
