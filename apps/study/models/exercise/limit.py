"""Exercise availability for the user."""

from typing import Final

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext as _

from apps.core.models import AbstractBaseModel

LIMIT_CHOICES: Final[dict[str, tuple[str, ...]]] = {
    'model__in': ('assignedcalculationcondition',)
}


class PeriodExecuting(models.TextChoices):
    """Exercise period executing choices."""

    DAILY = _('Daily')
    APPOINTMENT = _('By appointment as a mentor')


class ExerciseAvailability(AbstractBaseModel):
    """Exercise availability for the user."""

    count = models.PositiveSmallIntegerField(
        verbose_name=_('exercise.availability.count'),
    )
    period = models.CharField(
        max_length=30,
        choices=PeriodExecuting,
        verbose_name=_('exercise.availability.period'),
    )

    user = models.ForeignKey(
        'users.Person',
        on_delete=models.CASCADE,
        related_name='exercise_availabilities',
        verbose_name=_('exercise.availability.user'),
    )

    exercise_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=LIMIT_CHOICES,
    )
    exercise_object_id = models.PositiveIntegerField()
    exercise = GenericForeignKey('exercise_content_type', 'exercise_object_id')

    class Meta:
        """Model configuration."""

        verbose_name = _('Exercise availability')
        verbose_name_plural = _('Exercise availabilities')

        db_table = 'study_exercise_availability'
