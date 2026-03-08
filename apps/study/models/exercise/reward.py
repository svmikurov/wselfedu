"""Exercise reward model."""

from typing import Final

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext as _

from apps.core.models import AbstractBaseModel

LIMIT_CHOICES: Final[dict[str, tuple[str, ...]]] = {
    'model__in': ('studentcalculationcondition',)
}


class RewardType(models.TextChoices):
    """Reward type choice."""

    PER_CASE = _('Per each case')
    COMPLETE = _('For all cases')


class ExerciseReward(AbstractBaseModel):
    """Exercise reward."""

    exercise_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=LIMIT_CHOICES,
    )
    exercise_object_id = models.PositiveIntegerField()
    exercise = GenericForeignKey('exercise_content_type', 'exercise_object_id')

    reward_type = models.CharField(
        max_length=30,
        choices=RewardType,
        verbose_name=_('exercise.reward.type'),
    )

    amount = models.DecimalField(
        verbose_name=_('exercise.reward.amount'),
        max_digits=5,
        decimal_places=2,
    )

    class Meta:
        """Model configuration."""

        verbose_name = _('Exercise reward')
        verbose_name_plural = _('Exercise rewards')

        db_table = 'study_exercise_reward'
