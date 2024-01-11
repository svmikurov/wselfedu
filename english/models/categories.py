from django.db import models


class CategoryModel(models.Model):
    name = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        verbose_name='Наименование категории',
        help_text='Наименование не более 30 символов.'
    )
    description = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Описание.',
        help_text='Описание не более 100 символов.'
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name
