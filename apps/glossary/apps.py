"""Glossary app config."""

from django.apps import AppConfig


class GlossaryConfig(AppConfig):
    """Glossary app config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.glossary'

    verbose_name = 'Глоссарий'
    verbose_name_plural = 'Глоссарий'
