"""The Glossary application configuration module."""

from django.apps import AppConfig


class GlossaryConfig(AppConfig):
    """The Glossary application configuration."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'glossary'
