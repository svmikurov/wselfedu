"""Defines Mathematical application config."""

from django.apps import AppConfig


class MathConfig(AppConfig):
    """Mathematical application config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.math'
