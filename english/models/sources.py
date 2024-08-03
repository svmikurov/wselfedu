from django.db import models

from users.models import UserModel


class SourceModel(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Источник',
        help_text='Не более 50 символов.',
    )
    user = models.ForeignKey(
        UserModel,
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
        verbose_name = 'Источник'
        verbose_name_plural = 'Источники'
        ordering = ['name']

    def __str__(self):
        return self.name
