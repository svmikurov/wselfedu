"""Defines Study app config."""

from django.apps import AppConfig


class StudyConfig(AppConfig):
    """Study app config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.study'

    verbose_name = 'Обучение'
    verbose_name_plural = 'Обучения'
