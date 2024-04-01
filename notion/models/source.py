from django.db import models


class SourceModel(models.Model):
    """Модель источник определения."""

    name = models.CharField(max_length=64, blank=True)
    url = models.URLField()
    description = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name
