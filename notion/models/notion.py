from django.utils import timezone

from django.db import models

from notion.models import (
    CategoryModel,
    SourceModel,
)


class NotionModel(models.Model):
    """Модель определения."""

    name = models.CharField(
        max_length=64,
    )
    meaning = models.CharField(
        max_length=256,
    )
    category = models.ForeignKey(
        CategoryModel,
        on_delete=models.CASCADE,
        blank=True)
    source = models.ForeignKey(
        SourceModel,
        on_delete=models.CASCADE,
        blank=True)
    created_at = models.DateField(
        default=timezone.now
    )

    def __str__(self):
        return self.name
