"""Term model module."""

from django.db import models
from django.urls import reverse

from contrib.models import Category, Source
from contrib.models.params import ExerciseParams
from users.models import UserApp


class TermCategory(Category):
    """Model of the category of a glossary term."""


class TermSource(Source):
    """Model of the source of a glossary term."""


class Term(models.Model):
    """Term model class."""

    user = models.ForeignKey(
        UserApp,
        on_delete=models.CASCADE,
    )
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
        TermCategory,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Категория',
    )
    source = models.ForeignKey(
        TermSource,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Источник',
    )
    progress = models.DecimalField(
        max_digits=2,
        decimal_places=0,
        default=0,
    )
    """Numerical representation of study progress.
    """
    favorites = models.BooleanField(
        default=False,
        verbose_name='Избранное',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Изменено',
    )

    class Meta:
        """Set model features."""

        verbose_name = 'Глоссарий'
        verbose_name_plural = 'Глоссарий'
        ordering = ['pk']

    def __str__(self) -> str:
        """Provide the informal string representation of an object."""
        return self.term

    def get_absolute_url(self) -> str:
        """Return url to term detail page."""
        return reverse('glossary:term_detail', kwargs={'pk': self.pk})


class GlossaryParams(ExerciseParams):
    """User default settings for selecting terms in an exercise."""

    category = models.ForeignKey(
        TermCategory,
        models.SET_NULL,
        blank=True,
        null=True,
    )
    """If a category is selected, term from the specific source will be
    displayed.
    """
    source = models.ForeignKey(
        TermSource,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Источник',
    )
    """If a source is selected, term from the specific source will be
    displayed.
    """

    class Meta:
        """Set model features."""

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Настройки изучения терминов пользователей'

    def __str__(self) -> str:
        """Provide the informal string representation of an object."""
        return str(self.user)
