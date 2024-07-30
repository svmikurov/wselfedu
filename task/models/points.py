"""User points story."""

from django.db import models

from task.models.exercises_math import MathematicalExercise
from users.models import Guardianship, UserModel


class Points(models.Model):
    """User points model.

    For the correct execution of the exercise, the user receives points.
    This model stores the history of the user's points, their receipt,
    write-off and the balance of points at the current moment.
    """

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    """User owner of points.
    """
    task = models.ForeignKey(MathematicalExercise, on_delete=models.CASCADE)
    """The task for which points were awarded.
    """
    receipt = models.SmallIntegerField()
    """Amount of points awarded.
    """
    write_off = models.SmallIntegerField()
    """Amount of points written off.
    """
    balance = models.SmallIntegerField()
    """Current balance of points.
    """
    guardianship = models.ForeignKey(
        Guardianship,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    """Guardianship by virtue of which points are written off.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    """Date and time of creation of the record in the table.
    """
