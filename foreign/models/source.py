"""Word study source module."""

from django.db import models

from config.constants import NAME
from users.models import UserApp


class WordSource(models.Model):
    """Word study source model."""

    name = models.CharField(
        max_length=50,
        verbose_name='Источник',
        help_text='Не более 50 символов.',
    )
    user = models.ForeignKey(
        UserApp,
        on_delete=models.CASCADE,
    )
    url = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='URL-адрес источника',
    )
    description = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Описание',
        help_text='Не более 100 символов.',
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        """Set model features."""

        verbose_name = 'Источник'
        verbose_name_plural = 'Источники'
        ordering = [NAME]

    def __str__(self) -> str:
        """Provide the informal string representation of an object."""
        return self.name
