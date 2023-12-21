from django.db import models


class SourceModel(models.Model):
    name = models.CharField(
        max_length=50,
        blank=False, null=False,
        verbose_name='Источник',
        help_text='Не более 50 символов',
    )
    url = models.URLField(
        max_length=255,
        blank=True, null=True,
        verbose_name='Ссылка',
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Источник'
        verbose_name_plural = 'Источники'

    def __str__(self):
        return self.name
