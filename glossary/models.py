"""Glossary model module."""

from django.db import models

from config import constants as const
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

        unique_together = [[const.USER, const.TERM]]
        verbose_name = 'Прогресс'

    def __str__(self) -> str:
        """Provide the informal string representation of an object."""
        return self.progres


class GlossaryExerciseParams(models.Model):
    """User default settings for selecting terms in an exercise."""

    DEFAULT_START_PERIOD_INDEX = 0
    DEFAULT_END_PERIOD_INDEX = -1
    DEFAULT_PROGRES_INDEX = 0
    ALIAS_INDEX = 0

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
    )
    """User, (`UserModel`).
    """
    period_start_date = models.CharField(
        choices=const.EDGE_PERIOD_CHOICES,
        default=const.DEFAULT_START_PERIOD,
    )
    """A beginning of the period of adding a term to the glossary,
    :obj:`~config.constants.EDGE_PERIOD_CHOICES`
    (`list(tuple[str, str])`).
    """
    period_end_date = models.CharField(
        choices=const.EDGE_PERIOD_CHOICES,
        default=const.DEFAULT_END_PERIOD,
    )
    """An end of the period of adding a term to the glossary,
    :obj:`~config.constants.EDGE_PERIOD_CHOICES`
    (`list(tuple[str, str])`).
    """
    category = models.ForeignKey(
        GlossaryCategory,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    """A term category (`GlossaryCategory`).
    """
    progres = models.CharField(
        choices=const.PROGRES_CHOICES,
        default=const.DEFAULT_PROGRES,
    )
    """A term progres,
    :obj:`~task.forms.english_translate_choice_form.py.PROGRES_CHOICES`
    (`tuple[tuple[str, str]]`).
    """

    class Meta:
        """Set model features."""

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Настройки изучения терминов пользователей'

    def __str__(self) -> str:
        """Provide the informal string representation of an object."""
        return str(self.user)
