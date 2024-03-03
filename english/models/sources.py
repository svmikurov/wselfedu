from django.db import models

from users.models import UserModel


class SourceModel(models.Model):
    name = models.CharField(
        max_length=50,
        blank=False, null=False,
        verbose_name='Источник',
        help_text='Имя не более 50 символов.',
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    url = models.URLField(
        max_length=255,
        blank=True, null=True,
        verbose_name='Ссылка',
        help_text='URL-адрес источника.'
    )
    description = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name='Описание',
        help_text='Описание не более 100 слов.'
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Источник'
        verbose_name_plural = 'Источники'
        ordering = ['name']

    def __str__(self):
        return self.name
