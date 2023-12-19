from django.db import models


class LabelModel(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
        null=False, blank=False,
        verbose_name='Наименование метки',
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Метка'
        verbose_name_plural = 'Метки'
