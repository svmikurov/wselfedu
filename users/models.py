"""
The users app models module.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy


class UserModel(AbstractUser):
    """User model."""

    updated_at = models.DateTimeField(auto_now_add=True)
    """Date the user data was updated.
    """

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        """Represent an instance as a string."""
        return self.username

    def get_absolute_url(self) -> str:
        """Return the url of an instance."""
        return reverse_lazy('users:detail', kwargs={'pk': self.pk})


class Guardianship(models.Model):
    """Class representing the guardian-ward relationship.

    Guardian - a user who can assign tasks to a ward and view his or
    her solutions to tasks.
    The guardian determines the method of encouraging the ward for
    completing the exercise and provides a reward for successfully
    solving the problems.
    The custodian can carry out operations to write off the ward's
    points when encouraging.

    A guardian may have several wards, and vice versa.
    But the relationship between the guardian and the user must be
    unique.
    """

    guardian = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='guardian',
    )
    """The guardian user.
    """
    ward = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='ward',
    )
    """The ward user.
    """

    class Meta:
        """Meta class."""

        unique_together = ['guardian', 'ward']
        """The guardian-user relationship must be unique.
        """
