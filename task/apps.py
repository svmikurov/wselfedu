"""Configuration module of the Task application."""

from django.apps import AppConfig


class TaskConfig(AppConfig):
    """Configuration of the Task application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task'
