"""The Task application configuration module."""

from django.apps import AppConfig


class TaskConfig(AppConfig):
    """The Task application configuration."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task'
