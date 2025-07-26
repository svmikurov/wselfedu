"""Defines Lang app config."""

from django.apps import AppConfig


class LangConfig(AppConfig):
    """Lang app config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.lang'

    verbose_name = 'Иностранный язык'
    verbose_name_plural = 'Иностранные языки'
