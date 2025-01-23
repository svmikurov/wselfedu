"""Configuration module of the Task application."""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Configuration of the User application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Пользователи'
