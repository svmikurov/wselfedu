"""Defines Core application config."""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Core application config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.main'
