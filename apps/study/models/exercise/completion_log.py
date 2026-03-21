"""Store exercise completion log model."""

from typing import Final

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext as _

from apps.core.models import AbstractBaseModel

LIMIT_CHOICES: Final[dict[str, tuple[str, ...]]] = {
    'model__in': ('studentcalculationcondition',)
}


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
