"""Application configuration."""

from django.apps import AppConfig


class ForeignConfig(AppConfig):
    """The Foreign words application configuration."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'foreign'
