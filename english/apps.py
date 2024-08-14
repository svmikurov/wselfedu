"""Application configuration."""

from django.apps import AppConfig


class EnglishConfig(AppConfig):
    """The English application configuration."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'english'
