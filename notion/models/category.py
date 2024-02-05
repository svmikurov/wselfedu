from django.db import models


class CategoryModel(models.Model):
    """Модель категория определений."""

    name = models.CharField(max_length=64)
    descriptions = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name
