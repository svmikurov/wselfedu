"""Defines Math app config."""

from django.apps import AppConfig


class MathConfig(AppConfig):
    """Math app config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.math'

    verbose_name = 'Математика'
    verbose_name_plural = 'Математика'
