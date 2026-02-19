"""Exercise reward model."""

from typing import Final

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext as _

from apps.core.models import AbstractBaseModel

LIMIT_CHOICES: Final[dict[str, tuple[str, ...]]] = {
    'model__in': ('assignedcalculationcondition',)
}


class ExerciseReward(AbstractBaseModel):
    """Exercise reward."""

    amount = models.PositiveSmallIntegerField(
        verbose_name=_('exercise.reward.amount'),
    )

    mentorship = models.ForeignKey(
        'users.Mentorship',
        on_delete=models.CASCADE,
        verbose_name=_('exercise.reward.mentorship'),
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

        verbose_name = _('Exercise reward')
        verbose_name_plural = _('Exercise rewards')

        db_table = 'study_exercise_reward'
