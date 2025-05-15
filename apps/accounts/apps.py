"""Defines Account application config."""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Account application config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
