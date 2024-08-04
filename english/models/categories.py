from django.db import models

from users.models import UserModel


class CategoryModel(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='Наименование категории',
        help_text='Не более 30 символов.',
    )
    user = models.ForeignKey(
        UserModel,
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
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name
