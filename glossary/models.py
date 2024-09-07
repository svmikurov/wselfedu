"""Glossary model module."""

from django.db import models

from task.forms.english_translate_choice_form import (
    EDGE_PERIOD_ALIASES,
    KNOWLEDGE_ASSESSMENT,
)
from users.models import UserModel


class GlossaryCategory(models.Model):
    """Glossary category model class."""

    category = models.CharField(max_length=50)
    url = models.URLField(blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Добавлено')

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


class GlossaryExerciseParameters(models.Model):
    """Glossary exercise settings story model."""

    START_INDEX = 0
    END_INDEX = -1
    DEFAULT_PERIOD_START = EDGE_PERIOD_ALIASES[END_INDEX]
    DEFAULT_PERIOD_END = EDGE_PERIOD_ALIASES[START_INDEX]

    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    period_start_date = models.CharField(
        choices=EDGE_PERIOD_ALIASES, default=DEFAULT_PERIOD_START
    )
    period_end_date = models.CharField(
        choices=EDGE_PERIOD_ALIASES, default=DEFAULT_PERIOD_END
    )
    category = models.ForeignKey(
        GlossaryCategory, on_delete=models.CASCADE, blank=True, null=True
    )
    progres = models.CharField(
        choices=KNOWLEDGE_ASSESSMENT, default=KNOWLEDGE_ASSESSMENT[START_INDEX]
    )

    class Meta:
        """Set model features."""

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Настройки изучения терминов пользователей'

    def __str__(self) -> str:
        """Provide the informal string representation of an object."""
        return str(self.user)
