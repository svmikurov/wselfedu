"""Student reward service."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, override

from django.db import transaction
from django.db.models import F

from apps.study.models import RewardType
from apps.users.models import Balance, Transaction

from .abstract import AbstractRewardService

if TYPE_CHECKING:
    from apps.math.domains.dto import ExerciseRewardDTO
    from apps.users.models.user import Person

__all__ = ('RewardService',)


class RewardService(AbstractRewardService):
    """Exercise reward service."""

    @override
    def increment(self, student: Person, reward: ExerciseRewardDTO) -> None:
        """Add reward."""
        if not (reward_amount := self._get_reward(reward)):
            return

        with transaction.atomic():
            Balance.objects.update_or_create(
                user=student,
                defaults={'total': F('total') + reward_amount},
                create_defaults={'total': reward_amount},
            )
            Transaction.objects.create(
                user=student,
                amount=reward_amount,
                type=Transaction.Operation.REWARD,
            )

    # HACK: Implement reward type
    def _get_reward(self, reward: ExerciseRewardDTO | None) -> Decimal | None:
        if reward and reward.reward_type is RewardType.PER_CASE:
            return reward.reward_amount
        return None
