from django.db import models

from notion.models import (
    CategoryModel,
    SourceModel,
)


class NotionModel(models.Model):
    """Модель определения."""

    name = models.CharField(max_length=64)
    meaning = models.CharField(max_length=256)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    source = models.ForeignKey(SourceModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

