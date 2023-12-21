from django.db import models


class CategoryModel(models.Model):
    name = models.CharField(
        max_length=30,
        null=False,
        blank=False,
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
