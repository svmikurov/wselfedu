"""Education data source."""

from django.contrib.auth import get_user_model
from django.db import models


class Source(models.Model):
    """Education data source."""

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
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

    def __str__(self) -> str:
        """Get model instance string representation."""
        return str(self.name)
