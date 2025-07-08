"""Defines custom user model."""

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Custom user model."""

    class Meta:
        """Configure the model."""

        db_table = 'users_custom_user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
