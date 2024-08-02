"""The users app models module."""

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
