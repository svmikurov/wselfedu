"""Defines foreign app config."""

from django.apps import AppConfig


class ForeignConfig(AppConfig):
    """Foreign app config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.foreign'
