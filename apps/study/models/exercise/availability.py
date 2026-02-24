"""Exercise availability for the user."""

from typing import Final

from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRelation,
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

    required_count = models.PositiveSmallIntegerField(
        verbose_name=_('exercise.availability.count'),
    )
    period_type = models.CharField(
        max_length=30,
        choices=PeriodExecuting,
        verbose_name=_('exercise.availability.period'),
    )

    # The exercise can be assigned
    # by a mentor or by a user for self-study.
    user = models.ForeignKey(
        'users.Person',
        on_delete=models.CASCADE,
        related_name='exercise_availabilities',
        verbose_name=_('exercise.availability.user'),
    )

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

    # Exercise relationship
    exercise_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=LIMIT_CHOICES,
    )
    exercise_object_id = models.PositiveIntegerField()
    exercise = GenericForeignKey('exercise_content_type', 'exercise_object_id')

    exercise_logs = GenericRelation(
        'ExerciseLog',
        related_query_name='exercise_availability',
    )

    class Meta:
        """Model configuration."""

        verbose_name = _('Exercise availability')
        verbose_name_plural = _('Exercise availabilities')

        constraints = [
            models.UniqueConstraint(
                fields=[
                    'exercise_content_type',
                    'exercise_object_id',
                    'user',
                ],
                name='unique_exercise_availability',
            )
        ]

        db_table = 'study_exercise_availability'


class ExerciseLog(AbstractBaseModel):
    """Exercise performing log."""

    assigned_exercise = models.ForeignKey(
        ExerciseAvailability,
        on_delete=models.CASCADE,
        verbose_name='Assigned exercise for performing',
    )
    success_count = models.PositiveSmallIntegerField(
        verbose_name=_('Count of success task performing'),
    )
    failure_count = models.PositiveBigIntegerField(
        verbose_name=_('Count of failure task performing'),
    )

    tracking_date = models.DateField(
        verbose_name=_('Date for daily progress calculation'),
    )

    class Meta:
        """Model configuration."""

        verbose_name = _('Exercise performance log')
        verbose_name_plural = _('Exercise performance logs')

        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['assigned_exercise', 'tracking_date']),
            models.Index(fields=['tracking_date']),
        ]
        db_table = 'study_exercise_log'
