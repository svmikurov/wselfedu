"""Defines app model.

Model contains Django project applications enumeration.
"""

from django.db import models


class Apps(models.Model):
    """Project application model."""

    name = models.CharField(
        max_length=15,
        verbose_name='Имя приложения',
    )

    class Meta:
        """Model configuration."""

        db_table = 'main"."apps'
