"""The users app models module."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy


class UserApp(AbstractUser):
    """User model."""

    updated_at = models.DateTimeField(auto_now_add=True)
    """Date the user data was updated (`DateTimeField`).
    """

    class Meta:
        """Set model features."""

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_absolute_url(self) -> str:
        """Return the url of an instance."""
        return reverse_lazy('users:detail', kwargs={'pk': self.pk})

    def __str__(self) -> str:
        """Provide the informal string representation of an object."""
        return self.username
