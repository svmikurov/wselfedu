"""Defines user model."""

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """User model."""

    class Meta:
        """Model configuration."""

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
