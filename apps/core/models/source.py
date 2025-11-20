"""Education data source."""

from django.db import models


class Source(models.Model):
    """Education data source."""

    name = models.CharField(
        max_length=100,
        verbose_name='Источник',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Изменено',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Источник'
        verbose_name_plural = 'Источники'
