"""Exercise availability for the user."""

from typing import Final

from django.contrib.contenttypes.fields import (
    GenericForeignKey,
)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext as _

from apps.core.models import AbstractBaseModel

LIMIT_CHOICES: Final[dict[str, tuple[str, ...]]] = {
    'model__in': ('studentcalculationcondition',)
}


class PeriodExecuting(models.TextChoices):
    """Exercise period executing choices."""

    DAILY = _('Daily')
    APPOINTMENT = _('By appointment as a mentor')


class ExerciseAvailability(AbstractBaseModel):
    """Exercise availability for the user."""

    # Exercise relationship
    exercise_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=LIMIT_CHOICES,
    )
    exercise_object_id = models.PositiveIntegerField()
    exercise = GenericForeignKey('exercise_content_type', 'exercise_object_id')

    required_count = models.PositiveSmallIntegerField(
        verbose_name=_('exercise.availability.count'),
    )
    period_type = models.CharField(
        max_length=30,
        choices=PeriodExecuting,
        verbose_name=_('exercise.availability.period'),
    )

    # FIXME: Rename to 'assigned_at'
    # Only when reassigned (new target)
    started_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Date and time of exercise assignation'),
    )
    # Set by the user assigning the exercise
    is_active = models.BooleanField(
        default=False,
        verbose_name=_('Is the exercise active to perform?'),
    )
    # Programmatically set to True when all tasks are completed
    is_completed = models.BooleanField(
        default=False,
        verbose_name=_('Is the exercise fully completed?'),
    )
    # When is_completed became True
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Date and time of exercise assignation'),
    )

    class Meta:
        """Model configuration."""

        verbose_name = _('Exercise availability')
        verbose_name_plural = _('Exercise availabilities')

        db_table = 'study_exercise_availability'


class ExerciseLog(AbstractBaseModel):
    """Exercise performing log."""

    exercise_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=LIMIT_CHOICES,
    )
    exercise_object_id = models.PositiveIntegerField()
    exercise = GenericForeignKey('exercise_content_type', 'exercise_object_id')

    success_count = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_('Count of success task performing'),
    )
    failure_count = models.PositiveBigIntegerField(
        default=0,
        verbose_name=_('Count of failure task performing'),
    )

    tracking_date = models.DateField(
        auto_now=True,
        verbose_name=_('Date for daily progress tracking'),
    )

    class Meta:
        """Model configuration."""

        verbose_name = _('Exercise performance log')
        verbose_name_plural = _('Exercise performance logs')

        ordering = ['-created_at']

        db_table = 'study_exercise_log'
