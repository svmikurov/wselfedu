"""Glossary model module."""

from django.db import models


class GlossaryCategory(models.Model):
    """Glossary category model class."""

    category = models.CharField(max_length=50)
    url = models.URLField(blank=True)
    created_at = models.DateField(auto_created=True, verbose_name='Добавлено')

    class Meta:
        """Set model features."""

        verbose_name = 'Категория'
        verbose_name_plural = 'Категория'

    def __str__(self) -> str:
        """Provide the informal string representation of an object."""
        return self.category


class Glossary(models.Model):
    """Glossary model class."""

    term = models.CharField(
        max_length=50,
        verbose_name='Термин',
    )
    translate = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Перевод',
    )
    definition = models.CharField(
        max_length=250,
        blank=True,
        verbose_name='Определение',
    )
    interpretation = models.TextField(
        blank=True,
        verbose_name='Толкование',
    )
    category = models.ForeignKey(
        GlossaryCategory,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Категория',
    )
    created_at = models.DateField(auto_now_add=True, verbose_name='Добавлено')

    class Meta:
        """Set model features."""

        verbose_name = 'Глоссарий'
        verbose_name_plural = 'Глоссарий'

    def __str__(self) -> str:
        """Provide the informal string representation of an object."""
        return self.term
