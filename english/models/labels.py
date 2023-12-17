from django.db import models


class LabelModel(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
        null=False, blank=False,
        verbose_name='Наименование метки',
    )

    def __str__(self):
        return self.name
