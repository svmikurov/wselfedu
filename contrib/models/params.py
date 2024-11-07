"""User task settings model."""

from django.contrib.postgres.fields import ArrayField
from django.db import models

from config import constants as const
from config.constants import (
    DEFAULT_PROGRESS,
    DEFAULT_TIMEOUT,
    NOT_CHOICES,
    TODAY,
)
from users.models import UserApp


class ExerciseParams(models.Model):
    """Item learning exercise user parameters, abstract class.

    The general exercise parameters for learning them.
    """

    user = models.OneToOneField(
        UserApp,
        on_delete=models.CASCADE,
    )
    """User that setting model stored (`UserApp`).
    """
    timeout = models.PositiveSmallIntegerField(
        default=DEFAULT_TIMEOUT,
        verbose_name='Таймаут',
    )
    """Time to display question, sec (`int`).
    """
    favorites = models.BooleanField(
        default=False,
        verbose_name='Избранное',
    )
    """Will be display only favorites items if `True`, all otherwise
    (`bool`).
    """
    progress = ArrayField(
        models.CharField(max_length=16),
        default=DEFAULT_PROGRESS,
        verbose_name='Уровень знания',
    )
    """Current item learning progress level (`list[str]`).
    """
    period_start_date = models.CharField(
        choices=const.EDGE_PERIOD_CHOICES,
        default=NOT_CHOICES,
        verbose_name='Добавлено после',
    )
    """A beginning of the period of adding a item to study,
    :obj:`~config.constants.EDGE_PERIOD_CHOICES`
    (`list(tuple[str, str])`).
    """
    period_end_date = models.CharField(
        choices=const.EDGE_PERIOD_CHOICES,
        default=TODAY,
        max_length=2,
        verbose_name='Добавлено до',
    )
    """An end of the period of adding a item to study,
    :obj:`~config.constants.EDGE_PERIOD_CHOICES`
    (`list(tuple[str, str])`).
    """
    count_first = models.PositiveSmallIntegerField(
        default=0,
    )
    """Count of first added items (`int`).
    """
    count_last = models.PositiveSmallIntegerField(
        default=0,
    )
    """Count of last added items (`int`).
    """

    class Meta:
        """Model settings."""

        abstract = True
