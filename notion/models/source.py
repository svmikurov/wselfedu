from django.db import models


class SourceModel(models.Model):
    """Модель источник определения."""

    name = models.CharField(max_length=64, blank=True)
    url = models.URLField()

    def __str__(self):
        return self.name
