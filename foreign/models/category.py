"""Word category module."""

from django.db import models

from config.constants import NAME
from users.models import UserApp


class WordCategory(models.Model):
    """Word category model."""

    name = models.CharField(
        max_length=30,
        verbose_name='Наименование категории',
        help_text='Не более 30 символов.',
    )
    user = models.ForeignKey(
        UserApp,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    description = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Описание.',
        help_text='Не более 100 символов.',
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        """Set model features."""

        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = [NAME]

    def __str__(self) -> str:
        """Provide the informal string representation of an object."""
        return self.name
