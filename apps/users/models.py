"""Defines custom user model."""

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Custom user model."""

    class Meta:
        """Set model features."""

        app_label = 'users'

    def __str__(self) -> str:
        """Return the string representation."""
        return self.username
