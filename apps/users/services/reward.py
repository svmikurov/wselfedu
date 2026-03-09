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
    def increment(
        self,
        student: Person,
        reward: ExerciseRewardDTO,
        is_completed: bool,
    ) -> None:
        """Add reward."""
        if not (reward_amount := self._get_reward(reward, is_completed)):
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

    def _get_reward(
        self,
        reward: ExerciseRewardDTO | None,
        is_completed: bool,
    ) -> Decimal | None:
        if reward is None:
            return None

        if reward.reward_type is RewardType.PER_CASE:
            return reward.reward_amount

        if reward.reward_type is RewardType.COMPLETE and is_completed:
            return reward.reward_amount

        return None
