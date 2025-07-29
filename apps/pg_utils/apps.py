"""Defines pg_utils app config."""

from django.apps import AppConfig


class PgUtilsConfig(AppConfig):
    """pg_utils app config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.pg_utils'
