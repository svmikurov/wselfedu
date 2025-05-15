"""Defines custom user model."""

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Custom user model."""

    def __str__(self) -> str:
        """Return the string representation."""
        return self.email
