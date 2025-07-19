"""Defines users app config."""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """User app config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'

    verbose_name = 'Пользователи'
