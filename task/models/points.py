"""User points story."""
from django.core.exceptions import ValidationError
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
    task = models.OneToOneField(
        MathematicalExercise,
        on_delete=models.CASCADE,
    )
    """The task for which points were awarded.
    """
    award = models.PositiveSmallIntegerField(blank=True, null=True)
    """Amount of points awarded.
    """
    write_off = models.PositiveSmallIntegerField(blank=True, null=True)
    """Amount of points written off.
    """
    balance = models.PositiveSmallIntegerField(default=0)
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

    def clean(self) -> None:
        """Validate the condition of adding entry.

        In one entry you can fill only one of the two fields,
        either ``award`` or ``write_off``.

        Raises
        ------
        ValidationError
            Raised if both fields ``award`` and ``write_off`` are added
            or if both fields ``award`` and ``write_off`` is ``null``.
        """
        super().clean()
        if self.award and self.write_off:
            raise ValidationError(
                "Only 'award' or 'write_off' field, not both",
            )
        elif not self.award and not self.write_off:
            raise ValidationError(
                "Fill 'award' or 'write_off' field.",
            )
