"""User model."""

from django.contrib.auth.models import AbstractUser


class Person(AbstractUser):
    """Custom user model for development and testing.

    Extends Django's AbstractUser to provide a flexible user model
    for the development environment.
    """

    class Meta:
        """Model configuration."""

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
