"""Defines app model.

Model contains Django project applications enumeration.
"""

from django.db import models


class App(models.Model):
    """Project application model."""

    name = models.CharField(
        max_length=50,
        verbose_name='Имя приложения',
    )
    schema_name = models.CharField(
        max_length=50,
        verbose_name='Имя схемы в БД',
    )

    class Meta:
        """Model configuration."""

        db_table = 'main"."app'
        verbose_name = 'Основное приложение'
