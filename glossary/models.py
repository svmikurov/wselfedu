"""Glossary model module."""

from django.db import models

from config.consts import TERM, USER
from task.forms.english_translate_choice_form import (
    EDGE_PERIOD_ALIASES,
    KNOWLEDGE_ASSESSMENT,
)
from users.models import UserModel


class GlossaryCategory(models.Model):
    """Glossary category model class."""

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    url = models.URLField(blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Добавлено')

    class Meta:
        """Set model features."""

        verbose_name = 'Категория'
        verbose_name_plural = 'Категория'

    def __str__(self) -> str:
        """Provide the informal string representation of an object."""
        return self.name


class Glossary(models.Model):
    """Glossary model class."""

    user = models.ForeignKey(
        UserModel,
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


class GlossaryProgress(models.Model):
    """Glossary terms study progres."""

    term = models.ForeignKey(
        Glossary,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )
    progres = models.DecimalField(
        max_digits=2,
        decimal_places=0,
        default=0,
    )
    """Numerical representation of study progress.
    """

    class Meta:
        """Model options."""

        unique_together = [[USER, TERM]]
        verbose_name = 'Прогресс'

    def __str__(self) -> str:
        """Provide the informal string representation of an object."""
        return self.progres


class GlossaryExerciseParams(models.Model):
    """Glossary exercise settings story model.

    Story default user parameters to select wth terms in exercise:
        - User - student;
        - Start and End periods of adding a term;
        - term Category;
        - Progres of term study, as knowledge assessment.
    """

    DEFAULT_START_PERIOD_INDEX = 0
    DEFAULT_END_PERIOD_INDEX = -1
    DEFAULT_PROGRES_INDEX = 0
    ALIAS_INDEX = 0
    DEFAULT_PERIOD_START = EDGE_PERIOD_ALIASES[DEFAULT_START_PERIOD_INDEX]
    DEFAULT_PERIOD_END = EDGE_PERIOD_ALIASES[DEFAULT_END_PERIOD_INDEX]

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
    )
    period_start_date = models.CharField(
        choices=EDGE_PERIOD_ALIASES,
        default=DEFAULT_PERIOD_START[ALIAS_INDEX],
    )
    period_end_date = models.CharField(
        choices=EDGE_PERIOD_ALIASES,
        default=DEFAULT_PERIOD_END[ALIAS_INDEX],
    )
    category = models.ForeignKey(
        GlossaryCategory,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    progres = models.CharField(
        choices=KNOWLEDGE_ASSESSMENT,
        default=KNOWLEDGE_ASSESSMENT[DEFAULT_PROGRES_INDEX][ALIAS_INDEX],
    )

    class Meta:
        """Set model features."""

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Настройки изучения терминов пользователей'

    def __str__(self) -> str:
        """Provide the informal string representation of an object."""
        return str(self.user)
