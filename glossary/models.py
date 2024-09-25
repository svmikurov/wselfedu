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
    """Glossary exercise settings story model.

    Story default user parameters to select wth terms in exercise:
        - User - student;
        - Start and End periods of adding a term;
        - term Category;
        - Progres of term study, as knowledge assessment.

    :cvar user: A user whose parameters are stored.
    :vartype user: UserModel
    :cvar period_start_date: A beginning of the period of adding a term
     to the glossary, :obj:`~config.constants.EDGE_PERIOD_CHOICES`.
    :vartype period_start_date: list(tuple[str, str])
    :cvar period_end_date: An end of the period of adding a term
     to the glossary, :obj:`~config.constants.EDGE_PERIOD_CHOICES`.
    :vartype period_end_date: list(tuple[str, str])
    :cvar category: A term category.
    :vartype category: GlossaryCategory
    :cvar progres: A term progres,
     :obj:`~task.forms.english_translate_choice_form.py.PROGRES_CHOICES`.
    :vartype progres: tuple[tuple[str, str]]
    """

    DEFAULT_START_PERIOD_INDEX = 0
    DEFAULT_END_PERIOD_INDEX = -1
    DEFAULT_PROGRES_INDEX = 0
    ALIAS_INDEX = 0

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
    )
    period_start_date = models.CharField(
        choices=const.EDGE_PERIOD_CHOICES,
        default=const.DEFAULT_START_PERIOD,
    )
    period_end_date = models.CharField(
        choices=const.EDGE_PERIOD_CHOICES,
        default=const.DEFAULT_END_PERIOD,
    )
    category = models.ForeignKey(
        GlossaryCategory,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    progres = models.CharField(
        choices=const.PROGRES_CHOICES,
        default=const.DEFAULT_PROGRES,
    )

    class Meta:
        """Set model features."""

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Настройки изучения терминов пользователей'

    def __str__(self) -> str:
        """Provide the informal string representation of an object."""
        return str(self.user)
