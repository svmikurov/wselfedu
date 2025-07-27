"""Defines app model.

Model contains Django project applications enumeration.
"""

from django.db import models


class App(models.Model):
    """Project application model."""

    name = models.CharField(
        max_length=50,
        verbose_name='Наименование',
    )
    schema_name = models.CharField(
        max_length=50,
        verbose_name='Схема в БД',
        help_text='Каждое приложение расположено в отдельной схеме Postgres',
    )

    class Meta:
        """Model configuration."""

        db_table = 'main"."app'
        verbose_name = 'Приложение'
        verbose_name_plural = 'Приложения'
