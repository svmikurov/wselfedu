"""Calculate solutions model modul."""

from django.db import models

from users.models import UserModel


class CalculateSolution(models.Model):
    """Calculate solutions model.

    This model stores user calculation tasks and user solutions.
    The model stores only mathematical calculation
    :ref:`tasks <calculate_task>`.

    Fields
    ------
    * user - User id performing the exercise.
    * data_time - Date and time of receiving the task.
    * solution_time - Task completion time.
    * first_operand - First operand of a mathematical expression.
    * second_operand - Second operand of a mathematical expression.
    * calculation_type - The symbolic representation of mathematical
      operator of task.
    * user_solution - User answer to the task.
    * is_correctly - Marking the user's solution to the task as correct.
    """

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    data_time = models.DateTimeField(auto_now_add=True)
    solution_time = models.TimeField(blank=True, null=True)
    first_operand = models.IntegerField(max_length=3)
    second_operand = models.IntegerField(max_length=3)
    calculation_type = models.CharField(max_length=5)
    user_solution = models.IntegerField(max_length=6, blank=True, null=True)
    is_correctly = models.BooleanField(blank=True, null=True)
