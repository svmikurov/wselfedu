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

DEFAULT_PARAMS = {
    'timeout': DEFAULT_TIMEOUT,
    'has_timeout': True,
    'favorites': False,
    'progress': DEFAULT_PROGRESS,
    'period_start_date': NOT_CHOICES,
    'period_end_date': TODAY,
    'is_first': False,
    'is_last': False,
    'count_first': 10,
    'count_last': 20,
}


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
    has_timeout = models.BooleanField(default=True)
    """Time for user answer, (`bool`).
    """
    timeout = models.PositiveSmallIntegerField(
        default=DEFAULT_PARAMS['timeout'],
        verbose_name='Таймаут',
    )
    """Time to display question, sec (`int`).
    """
    favorites = models.BooleanField(
        default=DEFAULT_PARAMS['favorites'],
        verbose_name='Избранное',
    )
    """Will be display only favorites items if `True`, all otherwise
    (`bool`).
    """
    progress = ArrayField(
        models.CharField(max_length=16),
        default=DEFAULT_PARAMS['progress'],
        verbose_name='Уровень знания',
    )
    """Current item learning progress level (`list[str]`).
    """
    period_start_date = models.CharField(
        choices=const.EDGE_PERIOD_CHOICES,
        default=DEFAULT_PARAMS['period_start_date'],
        verbose_name='Добавлено после',
    )
    """A beginning of the period of adding a item to study,
    :obj:`~config.constants.EDGE_PERIOD_CHOICES`
    (`list(tuple[str, str])`).
    """
    period_end_date = models.CharField(
        choices=const.EDGE_PERIOD_CHOICES,
        default=DEFAULT_PARAMS['period_end_date'],
        max_length=2,
        verbose_name='Добавлено до',
    )
    """An end of the period of adding a item to study,
    :obj:`~config.constants.EDGE_PERIOD_CHOICES`
    (`list(tuple[str, str])`).
    """
    is_first = models.BooleanField(default=False)
    """Display first added items (`bool`).
    """
    is_last = models.BooleanField(default=False)
    """Display last added items (`bool`).
    """
    count_first = models.PositiveSmallIntegerField(
        default=DEFAULT_PARAMS['count_first'],
    )
    """Count of first added items (`int`).
    """
    count_last = models.PositiveSmallIntegerField(
        default=DEFAULT_PARAMS['count_last'],
    )
    """Count of last added items (`int`).
    """

    class Meta:
        """Model settings."""

        abstract = True
